"""API для работы с видео"""
from flask import jsonify, request
from data.models.video import Video
from data.models.association_tables import user_like_video, user_dislike_video
from data import db_session
from flask_restful import Resource, abort
from flask_login import login_required, current_user


def abort_if_video_not_found(video_id):
    """Выводит ошибку 404 если не найдено видео с таким id"""
    db_sess = db_session.create_session()
    video = db_sess.query(Video).get(video_id)
    if not video:
        abort(404, message=f"Video {video_id} not found")


class VideoResource(Resource):
    """Ресурс для работы с видео"""
    def get(self, video_id):
        """Получить данные о видео с id = video_id"""
        abort_if_video_not_found(video_id)
        db_sess = db_session.create_session()
        video = db_sess.query(Video).get(video_id)
        return jsonify({'video': video.to_dict(
            only=('title', 'file_name', 'preview', 'description', 'created_date', 'user_id', 'is_private'))})

    @login_required
    def delete(self, video_id):
        """Удалить видео с id = video_id (можно только пользователю, который загрузил это видео)"""
        abort_if_video_not_found(video_id)
        db_sess = db_session.create_session()
        video = db_sess.query(Video).get(video_id)
        if current_user == video.user:
            delete_likes_query = user_like_video.delete().where(user_like_video.c.video_liked == video.id)
            db_sess.execute(delete_likes_query)
            delete_dislikes_query = user_dislike_video.delete().where(user_dislike_video.c.video_disliked == video.id)
            db_sess.execute(delete_dislikes_query)
            db_sess.delete(video)
            db_sess.commit()
            return jsonify({'success': 'OK'})
        abort(400, message="You don't have rights to delete this")

    @login_required
    def post(self, video_id):
        """Изменить видео с id = video_id (можно только пользователю, который загрузил это видео)"""
        abort_if_video_not_found(video_id)
        db_sess = db_session.create_session()
        video = db_sess.query(Video).get(video_id)
        if current_user == video.user:
            title = request.args.get('title', video.title)
            description = request.args.get('description', video.description)
            is_private = request.args.get('is_private', video.is_private, type=int)
            is_private = video.is_private if is_private not in (0, 1) else is_private
            video.title = title
            video.description = description
            video.is_private = is_private
            db_sess.commit()
            return jsonify({'success': 'OK'})
        abort(400, message="You don't have rights to edit this")

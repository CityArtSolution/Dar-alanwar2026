import logging
import difflib

from odoo import http
from odoo.http import request

from .api_base import (
    ApiBaseController, json_response, error_response,
    jwt_required, get_request_data,
)

_logger = logging.getLogger(__name__)


class VoiceApiController(ApiBaseController):

    @http.route('/api/voice/evaluate', type='http', auth='none',
                methods=['POST'], csrf=False, cors='*')
    @jwt_required
    def evaluate_voice(self, **kwargs):
        """Evaluate voice recognition result against expected text."""
        data = get_request_data()

        recognized_text = data.get('recognized_text', '').strip()
        expected_text = data.get('expected_text', '').strip()
        language = data.get('language', 'ar')
        student_id = data.get('student_id')
        content_item_id = data.get('content_item_id')

        if not recognized_text or not expected_text:
            return error_response('recognized_text and expected_text are required')

        # Calculate similarity score
        similarity = difflib.SequenceMatcher(
            None,
            recognized_text.lower(),
            expected_text.lower(),
        ).ratio()

        score = round(similarity * 100, 1)

        # Determine feedback level
        if score >= 90:
            feedback = 'excellent'
            feedback_ar = 'ممتاز'
        elif score >= 70:
            feedback = 'good'
            feedback_ar = 'جيد'
        elif score >= 50:
            feedback = 'fair'
            feedback_ar = 'مقبول'
        else:
            feedback = 'needs_practice'
            feedback_ar = 'يحتاج تمرين'

        # Log usage if content item provided
        if student_id and content_item_id:
            request.env['education.content.usage'].sudo().create({
                'student_id': int(student_id),
                'content_item_id': int(content_item_id),
                'duration_minutes': 1,
                'score': score,
                'completed': score >= 70,
            })

        return json_response({
            'score': score,
            'feedback': feedback,
            'feedback_ar': feedback_ar,
            'recognized_text': recognized_text,
            'expected_text': expected_text,
            'match_details': {
                'similarity_ratio': similarity,
                'language': language,
            },
        })

    @http.route('/api/voice/words', type='http', auth='none',
                methods=['GET'], csrf=False, cors='*')
    @jwt_required
    def get_practice_words(self, **kwargs):
        """Get words for voice practice based on content."""
        parent = request.parent
        children = self._get_parent_children(parent)

        student_id = kwargs.get('student_id')
        language = kwargs.get('language', 'ar')
        level = kwargs.get('level', 'beginner')

        # Return sample practice words
        # In production, these would come from content items
        words_ar = {
            'beginner': [
                {'word': 'بسم الله', 'transliteration': 'Bismillah'},
                {'word': 'السلام عليكم', 'transliteration': 'Assalamu Alaikum'},
                {'word': 'شكرا', 'transliteration': 'Shukran'},
                {'word': 'مدرسة', 'transliteration': 'Madrasa'},
                {'word': 'كتاب', 'transliteration': 'Kitab'},
            ],
            'intermediate': [
                {'word': 'الحمد لله رب العالمين',
                 'transliteration': 'Alhamdulillahi Rabbil Aalameen'},
                {'word': 'أنا أحب المدرسة',
                 'transliteration': 'Ana uhibbu al-madrasa'},
            ],
        }

        words_en = {
            'beginner': [
                {'word': 'Hello', 'transliteration': 'Hello'},
                {'word': 'Thank you', 'transliteration': 'Thank you'},
                {'word': 'School', 'transliteration': 'School'},
                {'word': 'Teacher', 'transliteration': 'Teacher'},
                {'word': 'Book', 'transliteration': 'Book'},
            ],
        }

        words = words_ar if language == 'ar' else words_en
        practice_list = words.get(level, words.get('beginner', []))

        return json_response({
            'language': language,
            'level': level,
            'words': practice_list,
        })

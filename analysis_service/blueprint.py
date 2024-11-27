
from flask import Blueprint, jsonify, current_app, request, send_file
from neo4j_service import AnalysisRepository
import json


analysis_bp = Blueprint('analysis', __name__)


@analysis_bp.route('/api/v1/analysis/patterns', methods=['GET'])
def analyze_patterns():
    # קבלת ערך min_amount מהבקשה (ברירת מחדל: 10,000)
    min_amount = request.args.get('min_amount', 10000, type=int)

    try:
        # בדיקה אם התוצאה קיימת כבר ב-Redis
        cache_key = f'patterns_{min_amount}'
        cached_result = current_app.redis_client.get(cache_key)

        if cached_result:
            # אם התוצאה נמצאה בזיכרון מטמון, מחזירים אותה
            return jsonify(json.loads(cached_result)), 200

        # יצירת מופע של AnalysisRepository
        analyzer = AnalysisRepository(current_app.neo4j_driver)

        # שליפת תוצאות מ-Neo4j
        patterns = analyzer.find_circular_patterns(min_amount)

        # שמירה בזיכרון מטמון Redis ל-1 שעה (3600 שניות)
        current_app.redis_client.setex(
            cache_key,
            3600,  # שעה
            json.dumps(patterns)
        )

        # החזרת התוצאות כ-JSON
        return jsonify(patterns), 200

    except Exception as e:
        # טיפול בשגיאה והחזרת הודעת שגיאה
        current_app.logger.error(f"Error in analyze_patterns: {e}")
        return jsonify({"error": "Internal server error"}), 500

@analysis_bp.route('/api/v1/analysis/metrics', methods=['GET'])
def get_metrics():
    timeframe = int(request.args.get('timeframe_hours', 44))
    cache_key = f'metrics_{timeframe}'

    # קודם כל בוא ננסה להביא מהקאש
    cached_metrics = current_app.redis_client.get(cache_key)
    if cached_metrics:
        return jsonify(json.loads(cached_metrics)), 200

    try:
        analyzer = AnalysisRepository(current_app.neo4j_driver)
        metrics = analyzer.calculate_metrics(timeframe)

        current_app.redis_client.setex(
            cache_key,
            600, # 10 minutes
        json.dumps(metrics)
        )

        return jsonify(metrics), 200
    except Exception as ex:
        print(ex)
        return jsonify({"error": str(ex)}), 500


@analysis_bp.route('/api/v1/analysis/visualization', methods=['GET'])
def get_visualization():
    min_amount = float(request.args.get('min_amount', 50_000))

    try:
        analyzer = AnalysisRepository(current_app.neo4j_driver)
        buffer = analyzer.generate_network_visualization(min_amount)

        return send_file(
            buffer,
            mimetype='image/png',
            as_attachment=True,
            download_name='network_visualization.png'
        )

    except Exception as ex:
        return jsonify({"error": str(ex)}), 500






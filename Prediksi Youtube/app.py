# app.py - Main Flask Application
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)
CORS(app)

class YouTubePredictor:
    def __init__(self):
        self.factors = {
            'current_subscribers': {'weight': 0.3, 'min': 0, 'max': 100000},
            'avg_views_per_video': {'weight': 0.25, 'min': 0, 'max': 50000},
            'videos_per_week': {'weight': 0.15, 'min': 0, 'max': 10},
            'avg_video_length': {'weight': 0.1, 'min': 1, 'max': 60},
            'thumbnail_quality': {'weight': 0.12, 'min': 1, 'max': 10},
            'title_optimization': {'weight': 0.08, 'min': 1, 'max': 10},
            'consistency': {'weight': 0.1, 'min': 1, 'max': 10},
            'seasonality': {'weight': 0.05, 'min': 1, 'max': 10},
            'trending_topic': {'weight': 0.08, 'min': 1, 'max': 10},
            'engagement': {'weight': 0.15, 'min': 1, 'max': 10},
            'seo_optimization': {'weight': 0.1, 'min': 1, 'max': 10},
            'collaborations': {'weight': 0.12, 'min': 0, 'max': 10},
            'social_media_promo': {'weight': 0.08, 'min': 1, 'max': 10}
        }
    
    def calculate_growth_rate(self, inputs):
        """Calculate monthly growth rate based on input factors"""
        
        # Base growth rate berdasarkan size channel
        current_subs = inputs.get('current_subscribers', 1000)
        base_growth_rate = max(0.02, 0.25 - (current_subs / 120000))
        
        # Content quality multiplier
        content_quality = (
            inputs.get('thumbnail_quality', 5) + 
            inputs.get('title_optimization', 5) + 
            inputs.get('engagement', 5)
        ) / 30
        content_multiplier = 0.5 + content_quality
        
        # Consistency and frequency multipliers
        frequency_multiplier = 1 + (inputs.get('videos_per_week', 2) * 0.12)
        consistency_multiplier = 1 + (inputs.get('consistency', 5) * 0.06)
        
        # SEO and optimization
        seo_multiplier = 1 + (inputs.get('seo_optimization', 5) * 0.08)
        
        # External factors
        seasonality_multiplier = 0.7 + (inputs.get('seasonality', 5) * 0.06)
        trending_multiplier = 1 + (inputs.get('trending_topic', 5) * 0.12)
        promo_multiplier = 1 + (inputs.get('social_media_promo', 5) * 0.05)
        collab_multiplier = 1 + (inputs.get('collaborations', 0) * 0.18)
        
        # Video length optimization (sweet spot: 10-15 minutes)
        video_length = inputs.get('avg_video_length', 10)
        if video_length <= 15:
            duration_multiplier = 1 + (video_length * 0.025)
        else:
            duration_multiplier = 1.375 - ((video_length - 15) * 0.025)
        
        # Calculate final growth rate
        final_growth_rate = (
            base_growth_rate * 
            content_multiplier * 
            frequency_multiplier * 
            consistency_multiplier * 
            seo_multiplier * 
            seasonality_multiplier * 
            trending_multiplier * 
            promo_multiplier * 
            collab_multiplier * 
            duration_multiplier
        )
        
        return max(0.01, min(0.5, final_growth_rate))  # Cap between 1% and 50%
    
    def predict_growth(self, inputs, months=12):
        """Predict channel growth for specified months"""
        
        growth_rate = self.calculate_growth_rate(inputs)
        
        predictions = []
        current_subs = inputs.get('current_subscribers', 1000)
        current_views = inputs.get('avg_views_per_video', 500)
        videos_per_week = inputs.get('videos_per_week', 2)
        
        for month in range(1, months + 1):
            # Add some randomness to simulate real-world variations
            monthly_variation = np.random.uniform(0.8, 1.2)
            monthly_growth = growth_rate * monthly_variation
            
            # Calculate new values
            current_subs = int(current_subs * (1 + monthly_growth))
            current_views = int(current_views * (1 + monthly_growth * 0.85))
            
            # Calculate estimated monthly views
            estimated_monthly_views = current_views * videos_per_week * 4
            
            predictions.append({
                'month': month,
                'month_name': f'Bulan {month}',
                'subscribers': current_subs,
                'avg_views_per_video': current_views,
                'estimated_monthly_views': estimated_monthly_views,
                'growth_rate': monthly_growth * 100
            })
        
        return predictions, growth_rate * 100
    
    def analyze_factors(self, inputs):
        """Analyze which factors are strong/weak"""
        
        analysis = []
        
        # Content Quality
        content_score = (
            inputs.get('thumbnail_quality', 5) + 
            inputs.get('title_optimization', 5) + 
            inputs.get('engagement', 5)
        ) / 3
        analysis.append({
            'factor': 'Kualitas Konten',
            'score': round(content_score, 1),
            'impact': 'Tinggi',
            'status': 'Baik' if content_score >= 7 else 'Perlu Diperbaiki'
        })
        
        # Consistency
        consistency_score = inputs.get('consistency', 5)
        analysis.append({
            'factor': 'Konsistensi',
            'score': consistency_score,
            'impact': 'Tinggi',
            'status': 'Baik' if consistency_score >= 7 else 'Perlu Diperbaiki'
        })
        
        # SEO & Optimization
        seo_score = inputs.get('seo_optimization', 5)
        analysis.append({
            'factor': 'SEO & Optimasi',
            'score': seo_score,
            'impact': 'Sedang',
            'status': 'Baik' if seo_score >= 7 else 'Perlu Diperbaiki'
        })
        
        # Upload Frequency
        freq_score = min(10, inputs.get('videos_per_week', 2) * 2.5)
        analysis.append({
            'factor': 'Frekuensi Upload',
            'score': freq_score,
            'impact': 'Sedang',
            'status': 'Baik' if freq_score >= 7 else 'Perlu Diperbaiki'
        })
        
        # External Factors
        external_score = (
            inputs.get('seasonality', 5) + 
            inputs.get('trending_topic', 5) + 
            inputs.get('social_media_promo', 5) + 
            inputs.get('collaborations', 0)
        ) / 4
        analysis.append({
            'factor': 'Faktor Eksternal',
            'score': round(external_score, 1),
            'impact': 'Sedang',
            'status': 'Baik' if external_score >= 6 else 'Perlu Diperbaiki'
        })
        
        return analysis
    
    def get_recommendations(self, inputs):
        """Generate personalized recommendations"""
        
        recommendations = []
        
        if inputs.get('thumbnail_quality', 5) < 7:
            recommendations.append({
                'category': 'Konten',
                'recommendation': 'Tingkatkan kualitas thumbnail - gunakan warna kontras dan ekspresi wajah yang menarik',
                'priority': 'Tinggi'
            })
        
        if inputs.get('consistency', 5) < 7:
            recommendations.append({
                'category': 'Jadwal',
                'recommendation': 'Buat jadwal upload yang konsisten dan informasikan ke audience',
                'priority': 'Tinggi'
            })
        
        if inputs.get('seo_optimization', 5) < 7:
            recommendations.append({
                'category': 'SEO',
                'recommendation': 'Lakukan riset keyword dan optimalkan judul, deskripsi, dan tags',
                'priority': 'Sedang'
            })
        
        if inputs.get('engagement', 5) < 6:
            recommendations.append({
                'category': 'Engagement',
                'recommendation': 'Tingkatkan interaksi dengan audience melalui Q&A dan respond komentar',
                'priority': 'Tinggi'
            })
        
        if inputs.get('social_media_promo', 5) < 6:
            recommendations.append({
                'category': 'Promosi',
                'recommendation': 'Manfaatkan platform media sosial lain untuk promosi cross-platform',
                'priority': 'Sedang'
            })
        
        if inputs.get('collaborations', 0) < 2:
            recommendations.append({
                'category': 'Kolaborasi',
                'recommendation': 'Cari peluang kolaborasi dengan creator lain di niche yang sama',
                'priority': 'Sedang'
            })
        
        if inputs.get('videos_per_week', 2) < 2:
            recommendations.append({
                'category': 'Frekuensi',
                'recommendation': 'Tingkatkan frekuensi upload minimal 2-3 video per minggu',
                'priority': 'Sedang'
            })
        
        if len(recommendations) == 0:
            recommendations.append({
                'category': 'Umum',
                'recommendation': 'Channel Anda sudah dioptimalkan dengan baik! Pertahankan konsistensi dan terus berinovasi',
                'priority': 'Maintenance'
            })
        
        return recommendations

# Initialize predictor
predictor = YouTubePredictor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        
        # Validate input data
        inputs = {}
        for key, value in data.items():
            if key in predictor.factors:
                factor_config = predictor.factors[key]
                # Clamp values to valid range
                inputs[key] = max(factor_config['min'], min(factor_config['max'], float(value)))
        
        # Generate predictions
        predictions, growth_rate = predictor.predict_growth(inputs)
        factor_analysis = predictor.analyze_factors(inputs)
        recommendations = predictor.get_recommendations(inputs)
        
        return jsonify({
            'success': True,
            'predictions': predictions,
            'growth_rate': round(growth_rate, 2),
            'factor_analysis': factor_analysis,
            'recommendations': recommendations,
            'summary': {
                'initial_subscribers': inputs.get('current_subscribers', 1000),
                'final_subscribers': predictions[-1]['subscribers'],
                'total_growth': predictions[-1]['subscribers'] - inputs.get('current_subscribers', 1000),
                'growth_percentage': round(((predictions[-1]['subscribers'] / inputs.get('current_subscribers', 1000)) - 1) * 100, 1)
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/factors')
def get_factors():
    """Get factor configuration for frontend"""
    return jsonify(predictor.factors)

# Create templates directory if it doesn't exist
os.makedirs('templates', exist_ok=True)

# Save HTML template
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

# Requirements.txt content
requirements = """
Flask==2.3.3
Flask-CORS==4.0.0
numpy==1.24.3
pandas==2.0.3
python-dateutil==2.8.2
"""

# Save requirements
with open('requirements.txt', 'w') as f:
    f.write(requirements)

if __name__ == '__main__':
    print("🚀 Starting YouTube Channel Predictor App...")
    print("📊 Access the app at: http://localhost:5000")
    print("🔧 API endpoint: http://localhost:5000/api/predict")
    print("📋 Factors endpoint: http://localhost:5000/api/factors")
    print("\n💡 Features:")
    print("   - Real-time prediction with 13+ factors")
    print("   - Interactive charts and visualizations")
    print("   - Personalized recommendations")
    print("   - 12-month growth forecasting")
    print("   - Factor analysis and optimization tips")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
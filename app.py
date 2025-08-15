from flask import Flask, render_template, jsonify, request
import os

app = Flask(__name__)
STATIC_DIR = os.path.join(app.root_path, 'static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/videos')
def list_videos():
    folders = [
        f for f in os.listdir(STATIC_DIR)
        if os.path.isdir(os.path.join(STATIC_DIR, f))
    ]

    videos = []
    for folder in folders:
        folder_path = os.path.join(STATIC_DIR, folder)
        for filename in os.listdir(folder_path):
            if filename.lower().endswith('.mp4'):
                video_path = os.path.join(folder_path, filename)
                size = os.path.getsize(video_path)

                category = filename.split(' ')[0].replace('#', '')
                thumb_name = filename.replace('.mp4', '.png')
                thumb_path = os.path.join(folder_path, thumb_name)
                has_thumb = os.path.exists(thumb_path)

                rel_video_path = f"{folder}/{filename}"
                rel_thumb_path = f"{folder}/{thumb_name}" if has_thumb else rel_video_path # 这里的修改！

                videos.append({
                    'name': filename,
                    'size': size,
                    'category': category,
                    'thumbnail': rel_thumb_path, # 这里现在要么是 .png 路径，要么是 .mp4 路径
                    'path': rel_video_path
                })

    return jsonify(videos)

@app.route('/api/delete', methods=['POST'])
def delete_video():
    data = request.json
    name = data['name']
    abs_path = os.path.join(STATIC_DIR, name)
    thumb_path = abs_path.replace('.mp4', '.png')
    try:
        os.remove(abs_path)
        if os.path.exists(thumb_path):
            os.remove(thumb_path)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/rename', methods=['POST'])
def rename_video():
    data = request.json
    old_path = os.path.join(STATIC_DIR, data['oldName'])
    new_path = os.path.join(STATIC_DIR, data['newName'])

    try:
        os.rename(old_path, new_path)

        old_thumb = old_path.replace('.mp4', '.png')
        new_thumb = new_path.replace('.mp4', '.png')
        if os.path.exists(old_thumb):
            os.rename(old_thumb, new_thumb)

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/open')
def open_folder():
    os.startfile(STATIC_DIR)
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run()

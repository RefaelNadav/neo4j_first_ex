
FROM python:3.9-slim

# הגדרת תיקיית עבודה בתוך הקונטיינר
WORKDIR /app

# העתקת קבצי requirements.txt לתוך הקונטיינר
COPY requirements.txt .


# התקנת כל התלויות
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


EXPOSE 5001


# הרצת הקובץ app.py
CMD ["python", "app.py"]

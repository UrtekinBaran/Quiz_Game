import random
from sqlalchemy import create_engine, Integer, String, Sequence
from sqlalchemy.orm import DeclarativeBase, sessionmaker, mapped_column

# "sequence" (dizi), genellikle veritabanlarında benzersiz anahtarları veya diğer otomatik artan değerleri
# üretmek için kullanılan bir veritabanı nesnesidir.

# Veritabanı bağlantısı
db_url = 'postgresql://kullanici_adi:sifre@localhost:5432/postgres'


# SQLAlchemy Engine oluşturma
engine = create_engine(db_url)


# Base sınıfını tanımlama
class Base(DeclarativeBase):
    pass


# Kullanıcılar tablosunu temsil eden model sınıfını oluşturma
class User(Base):
    __tablename__ = 'users'

    id = mapped_column(Integer, Sequence('user_id_seq'), primary_key=True)
    username = mapped_column(String(50), unique=True)
    score = mapped_column(Integer)


# sorular tablosunu temsil eden model sınıfı oluşturma
class Question(Base):
    __tablename__ = "questions"

    id = mapped_column(Integer, Sequence("question_id_seq"), primary_key=True)
    content = mapped_column(String(255), nullable=False)
    answer = mapped_column(String(50), nullable=False)

    # nullable=False: Bu, sütunun boş olamayacağını belirtir.


# veritabanındaki tabloları oluşturur.
Base.metadata.create_all(bind=engine)

# session veritabanı işlemleri için kullanılır, bize oturum sağlar.
Session = sessionmaker(bind=engine)
session = Session()
session.query(Question).all()

for q in session.query(Question).all():
    session.delete(q)
session.commit()

# örnek sorular
questions_data = [
    {"content": "Uncharted 4 bir hırsız'ın sonu ne zaman çıkışını gerçekleştirmiştir?", "answer": "2016"},
    {"content": "GOD OF War Ragnarök kaç adet satmıştır ?", "answer": "11 Milyon"},
    {"content": "THE LAST OF US PART II'nin baş yazarı kimdir", "answer": "Neil Druckmann"},
    {"content": "Baran'ın en sevdiği oyun hangisidir", "answer": "THE LAST OF US PART II"},
    {"content": "Resident evıl 4 remake'in ana karekteri kimdir", "answer": "Lion s. Kenndy"},
    {"content": "Cory barlog hangi studio'nun başındadır ", "answer": "Santa Monica"},
    {"content": "Marvel'ın en güçlü karekteri kimdir", "answer": "THOR"},
    {"content": "Marvel Spider-man 2 metacritic ortalaması kaçtır?", "answer": "90"},
    {"content": "Game Awards 2020 kazananı kimdir ", "answer": "the last of us part II"},
    {"content": "Avengers ekibini yenen kötü kahraman kimdir", "answer": "Thanos"},
    {"content": "Tony Stark'ın kızı babasını ne kadar seviyor:)", "answer": "üçbin kez"},
    {"content": "Spider-man no way homeda ki başrol oyuncusu kimdir?", "answer": "Tom Holland"},
    {"content": "Nathan Drake son macerası neydi ?", "answer": "Henry every'nin hazinesi"},
    {"content": "Thor'un çekici'nin adı nedir", "answer": "Mjolnir "},
    {"content": "GTA kaç milyon satmıştır", "answer": "180 milyon"},
    {"content": "RDR II'nin efsane karekteri kimdir", "answer": "Arthur Morgan"},
    {"content": "The last of us part I'de kontrol ettiğimiz efsane karekter kimdir", "answer": "Joel Milner"},
]

# bu döngü her bir data sözlüğü için yeni bir question nesnesi oluşturur ve nesneyi ekler
for data in questions_data:
    new_question = Question(content=data["content"], answer=data["answer"])
    session.add(new_question)

session.commit()

# kullanıcı ismi alma
username = input("Enter your username: ")
# kullanıcı adı alınır ve varsa veritabanından çekilir, yoksa yeni bir kullanacı eklenir.
user = session.query(User).filter_by(username=username).first()  # query bilgi çekmek için kullanılır.

if user is None:
    user = User(username=username, score=0)
    session.add(user)
    session.commit()
# kullanıcı adı veritabanında bulunmamışsa, yeni bir kullanıcı oluşturulur.


#  soru sorma fonksiyonu
def ask_question():
    questions = session.query(Question).all()  # Bu satır, veritabanındaki tüm soruları çeker ve questions adlı bir
    # liste içinde saklar.
    question = random.choice(questions)  # Bu satır, questions listesinden rastgele bir soru seçer
    print(f"Question: {question.content}")
    user_answer = input("Your answer: ").strip().lower()
    # cevap durumuna göre if veya else döndürür
    if user_answer == question.answer:
        print("Correct!")
        return True
    else:
        print("Wrong!")
        return False


# Bilgi yarışması oyunu
num_questions = 10  # İstediğiniz soru sayısını ayarlama
asked_questions = set()

for _ in range(num_questions):  # (_) kullanılmayan bir değişkenin yerine geçer.
    while True:  # Bu iç içe geçmiş döngü, bir soru seçilene kadar sürekli olarak çalışır.
        question = random.choice(session.query(Question).all())
        if question.id not in asked_questions:  # bu kodun açıklaması not defterinde unutma!!!
            asked_questions.add(question.id)
            break

    print(f"Question: {question.content}")
    user_answer = input("Your answer: ").strip().lower()  # Kullanıcının cevabını küçük harfe çeviriyoruz

    if user_answer == question.answer.lower():
        print("Correct!")
        user.score += 10
    else:
        print("Wrong!")

# Kullanıcı bilgilerini yazdırma
print(f"User: {user.username}, Score: {user.score}")

if user.score >= 100:
    print("A+! Congratulations!")
elif user.score >= 80:
    print("A! Well done!")
elif user.score >= 60:
    print("B! Good job!")
elif user.score >= 40:
    print("C! Not bad!")
elif user.score >= 20:
    print("D! Keep trying!")
elif user.score >= 10:
    print("E! You can do better!")
else:
    print("F! Better luck next time!")

# Skoru güncelleme ve kullanıcıyı kaydetme
session.commit()

# Kullanıcı bilgilerini yazdırma
print(f"User: {user.username}, Score: {user.score}")

# Session'ı kapatma
session.close()

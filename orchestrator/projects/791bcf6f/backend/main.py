from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
import os

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./court_department.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class News(Base):
    __tablename__ = "news"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    excerpt = Column(String(1000))
    image_url = Column(String(500))
    published_at = Column(DateTime, default=datetime.utcnow)
    is_published = Column(Boolean, default=True)
    category = Column(String(100), default="general")
    views = Column(Integer, default=0)

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    description = Column(Text)
    file_url = Column(String(500), nullable=False)
    file_size = Column(Integer)
    file_type = Column(String(50))
    category = Column(String(100))
    published_at = Column(DateTime, default=datetime.utcnow)
    downloads = Column(Integer, default=0)

class Appeal(Base):
    __tablename__ = "appeals"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    phone = Column(String(50))
    subject = Column(String(300), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="new")  # new, in_progress, resolved
    response = Column(Text)
    responded_at = Column(DateTime)

class Statistic(Base):
    __tablename__ = "statistics"
    
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False)
    region = Column(String(200))
    total_cases = Column(Integer, default=0)
    civil_cases = Column(Integer, default=0)
    criminal_cases = Column(Integer, default=0)
    arbitration_cases = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow)

# Pydantic Schemas
class NewsBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=500)
    content: str = Field(..., min_length=10)
    excerpt: Optional[str] = None
    image_url: Optional[str] = None
    category: str = "general"
    is_published: bool = True

class NewsCreate(NewsBase):
    pass

class NewsResponse(NewsBase):
    id: int
    published_at: datetime
    views: int
    
    class Config:
        from_attributes = True

class DocumentBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=500)
    description: Optional[str] = None
    file_url: str
    file_size: Optional[int] = None
    file_type: Optional[str] = None
    category: Optional[str] = None

class DocumentCreate(DocumentBase):
    pass

class DocumentResponse(DocumentBase):
    id: int
    published_at: datetime
    downloads: int
    
    class Config:
        from_attributes = True

class AppealBase(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=200)
    email: str = Field(..., regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    phone: Optional[str] = None
    subject: str = Field(..., min_length=5, max_length=300)
    message: str = Field(..., min_length=20)

class AppealCreate(AppealBase):
    pass

class AppealResponse(AppealBase):
    id: int
    created_at: datetime
    status: str
    response: Optional[str] = None
    responded_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class StatisticBase(BaseModel):
    year: int
    region: Optional[str] = None
    total_cases: int = 0
    civil_cases: int = 0
    criminal_cases: int = 0
    arbitration_cases: int = 0

class StatisticCreate(StatisticBase):
    pass

class StatisticResponse(StatisticBase):
    id: int
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI(
    title="Судебный департамент API",
    description="API для сайта Судебного департамента при Верховном Суде Российской Федерации",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В production указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# NEWS ENDPOINTS
@app.get("/api/news", response_model=List[NewsResponse])
def get_news(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Получить список новостей"""
    query = db.query(News).filter(News.is_published == True)
    if category:
        query = query.filter(News.category == category)
    news = query.order_by(News.published_at.desc()).offset(skip).limit(limit).all()
    return news

@app.get("/api/news/{news_id}", response_model=NewsResponse)
def get_news_item(news_id: int, db: Session = Depends(get_db)):
    """Получить одну новость"""
    news = db.query(News).filter(News.id == news_id, News.is_published == True).first()
    if not news:
        raise HTTPException(status_code=404, detail="Новость не найдена")
    # Increment views
    news.views += 1
    db.commit()
    return news

@app.post("/api/news", response_model=NewsResponse)
def create_news(news: NewsCreate, db: Session = Depends(get_db)):
    """Создать новость (для админки)"""
    if not news.excerpt:
        news.excerpt = news.content[:200] + "..." if len(news.content) > 200 else news.content
    
    db_news = News(**news.dict())
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news

@app.put("/api/news/{news_id}", response_model=NewsResponse)
def update_news(news_id: int, news_update: NewsCreate, db: Session = Depends(get_db)):
    """Обновить новость"""
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="Новость не найдена")
    
    for key, value in news_update.dict().items():
        setattr(news, key, value)
    
    db.commit()
    db.refresh(news)
    return news

@app.delete("/api/news/{news_id}")
def delete_news(news_id: int, db: Session = Depends(get_db)):
    """Удалить новость"""
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="Новость не найдена")
    db.delete(news)
    db.commit()
    return {"message": "Новость удалена"}

# DOCUMENTS ENDPOINTS
@app.get("/api/documents", response_model=List[DocumentResponse])
def get_documents(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Получить список документов"""
    query = db.query(Document)
    if category:
        query = query.filter(Document.category == category)
    documents = query.order_by(Document.published_at.desc()).offset(skip).limit(limit).all()
    return documents

@app.get("/api/documents/{doc_id}", response_model=DocumentResponse)
def get_document(doc_id: int, db: Session = Depends(get_db)):
    """Получить документ"""
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Документ не найден")
    return doc

@app.post("/api/documents", response_model=DocumentResponse)
def create_document(doc: DocumentCreate, db: Session = Depends(get_db)):
    """Создать документ"""
    db_doc = Document(**doc.dict())
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc

@app.post("/api/documents/{doc_id}/download")
def download_document(doc_id: int, db: Session = Depends(get_db)):
    """Увеличить счётчик скачиваний"""
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Документ не найден")
    doc.downloads += 1
    db.commit()
    return {"file_url": doc.file_url, "downloads": doc.downloads}

# APPEALS ENDPOINTS
@app.post("/api/appeals", response_model=AppealResponse)
def create_appeal(appeal: AppealCreate, db: Session = Depends(get_db)):
    """Создать обращение гражданина"""
    db_appeal = Appeal(**appeal.dict())
    db.add(db_appeal)
    db.commit()
    db.refresh(db_appeal)
    return db_appeal

@app.get("/api/appeals", response_model=List[AppealResponse])
def get_appeals(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Получить список обращений (для админки)"""
    query = db.query(Appeal)
    if status:
        query = query.filter(Appeal.status == status)
    appeals = query.order_by(Appeal.created_at.desc()).offset(skip).limit(limit).all()
    return appeals

@app.get("/api/appeals/{appeal_id}", response_model=AppealResponse)
def get_appeal(appeal_id: int, db: Session = Depends(get_db)):
    """Получить обращение"""
    appeal = db.query(Appeal).filter(Appeal.id == appeal_id).first()
    if not appeal:
        raise HTTPException(status_code=404, detail="Обращение не найдено")
    return appeal

@app.put("/api/appeals/{appeal_id}/respond")
def respond_to_appeal(appeal_id: int, response: str, db: Session = Depends(get_db)):
    """Ответить на обращение"""
    appeal = db.query(Appeal).filter(Appeal.id == appeal_id).first()
    if not appeal:
        raise HTTPException(status_code=404, detail="Обращение не найдено")
    
    appeal.response = response
    appeal.status = "resolved"
    appeal.responded_at = datetime.utcnow()
    db.commit()
    return appeal

# STATISTICS ENDPOINTS
@app.get("/api/statistics", response_model=List[StatisticResponse])
def get_statistics(
    year: Optional[int] = None,
    region: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Получить статистику"""
    query = db.query(Statistic)
    if year:
        query = query.filter(Statistic.year == year)
    if region:
        query = query.filter(Statistic.region == region)
    stats = query.order_by(Statistic.year.desc()).all()
    return stats

@app.post("/api/statistics", response_model=StatisticResponse)
def create_statistic(stat: StatisticCreate, db: Session = Depends(get_db)):
    """Добавить статистику"""
    db_stat = Statistic(**stat.dict())
    db.add(db_stat)
    db.commit()
    db.refresh(db_stat)
    return db_stat

@app.get("/api/statistics/summary")
def get_statistics_summary(db: Session = Depends(get_db)):
    """Сводная статистика"""
    latest_year = db.query(Statistic).order_by(Statistic.year.desc()).first()
    if not latest_year:
        return {"message": "Нет данных"}
    
    all_stats = db.query(Statistic).filter(Statistic.year == latest_year.year).all()
    
    total_cases = sum(s.total_cases for s in all_stats)
    civil = sum(s.civil_cases for s in all_stats)
    criminal = sum(s.criminal_cases for s in all_stats)
    arbitration = sum(s.arbitration_cases for s in all_stats)
    
    return {
        "year": latest_year.year,
        "total_cases": total_cases,
        "civil_cases": civil,
        "criminal_cases": criminal,
        "arbitration_cases": arbitration,
        "regions_count": len(all_stats)
    }

# HEALTH CHECK
@app.get("/api/health")
def health_check():
    """Проверка работоспособности API"""
    return {
        "status": "ok",
        "service": "Судебный департамент API",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

# SEED DATA
@app.post("/api/seed")
def seed_data(db: Session = Depends(get_db)):
    """Заполнить базу тестовыми данными"""
    # Добавляем новости
    news_items = [
        News(
            title="Проведены занятия по вопросам противодействия коррупции",
            content="В Судебном департаменте прошли обучающие занятия для сотрудников...",
            excerpt="В Судебном департаменте прошли обучающие занятия...",
            category="events",
            published_at=datetime(2026, 4, 1)
        ),
        News(
            title="Генеральный директор принял участие в заседании Совета судей РФ",
            content="В заседании обсуждались вопросы развития судебной системы...",
            excerpt="В заседании обсуждались вопросы развития...",
            category="meetings",
            published_at=datetime(2026, 3, 31)
        ),
    ]
    
    for news in news_items:
        db.add(news)
    
    # Добавляем документы
    docs = [
        Document(
            title="Приказ о противодействии коррупции",
            description="Основные положения приказа...",
            file_url="/docs/anticorruption.pdf",
            file_type="pdf",
            category="orders"
        ),
    ]
    
    for doc in docs:
        db.add(doc)
    
    # Добавляем статистику
    stats = [
        Statistic(year=2025, region="Москва", total_cases=150000, civil_cases=80000, criminal_cases=50000, arbitration_cases=20000),
        Statistic(year=2025, region="Санкт-Петербург", total_cases=80000, civil_cases=45000, criminal_cases=25000, arbitration_cases=10000),
    ]
    
    for stat in stats:
        db.add(stat)
    
    db.commit()
    return {"message": "Тестовые данные добавлены"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from experta import *
import uuid
from datetime import datetime

app = Flask(__name__)
CORS(app)

# ---------- ФАКТЫ ----------
class Film(Fact):
    #Факт о фильме
    pass

class Answer(Fact):
    #Ответ пользователя
    pass

class Stage(Fact):
    #Текущий этап
    pass

class Preference(Fact):
    #Предпочтение пользователя
    pass

class FilterCondition(Fact):
    #Условие фильтрации
    pass

class Recommendation(Fact):
    #Рекомендация фильма
    pass

class Context(Fact):
    #Контекст просмотра
    pass

class SkipReason(Fact):
    #Причина пропуска вопроса
    pass


class MovieExpertAPI:
    
    def __init__(self):
        self.sessions = {}
        self.all_films = self.load_films()
        self.stage_questions = self.create_stage_questions()
    
    def load_films(self):
        try:
            with open("films.json", "r", encoding="utf-8") as f:
                data = json.load(f)["films"]
            return data
        except FileNotFoundError:
            return [
                {
                    "id": 1,
                    "title": "Начало",
                    "original_title": "Inception",
                    "year": 2010,
                    "genres": ["science fiction", "thriller", "action"],
                    "mood": ["thoughtful", "intense", "mysterious"],
                    "energy_level": "high",
                    "duration": 148,
                    "rating": 8.8,
                    "director": "Кристофер Нолан",
                    "description": "Фильм о ворах, которые крадут идеи из подсознания.",
                    "parameters": {
                        "philosophical": 0.8,
                        "complexity": 0.9,
                        "visual": 0.95
                    },
                    "tags": ["сны", "реальность", "память"],
                    "features": {
                        "is_thought_provoking": True,
                        "is_fast_paced": True,
                        "has_plot_twist": True,
                        "is_emotional": False,
                        "has_happy_ending": True
                    },
                    "target_audience": {
                        "preferred_viewing": ["alone", "friends"],
                        "best_time": ["evening"]
                    },
                    "keywords": ["inception", "dream", "reality"]
                }
            ]
    
    def create_stage_questions(self):
        #Структура вопросов по стадиям
        return {
            'start': [
                {
                    'key': 'wants_thoughtful',
                    'text': 'Хотите фильм, который заставит задуматься?',
                    'type': 'yes_no',
                    'explanation': 'Интеллектуальные фильмы, поднимающие важные вопросы'
                },
                {
                    'key': 'wants_positive_mood',
                    'text': 'Нужен фильм для поднятия настроения?',
                    'type': 'yes_no',
                    'explanation': 'Фильмы, которые дарят радость и вдохновение'
                },
                {
                    'key': 'wants_tension',
                    'text': 'Хотите почувствовать напряжение и адреналин?',
                    'type': 'yes_no',
                    'explanation': 'Триллеры, хорроры, напряжённые драмы'
                },
                {
                    'key': 'current_emotion',
                    'text': 'Какая эмоция вам ближе сейчас?',
                    'type': 'multiple_choice',
                    'options': ["радость", "грусть", "тревога", "спокойствие", "вдохновение", "любовь"]
                }
            ],
            'energy': [
                {
                    'key': 'wants_fast_paced',
                    'text': 'Предпочитаете быстрый, динамичный темп?',
                    'type': 'yes_no',
                    'explanation': 'Быстрые монтажные склейки, много действий'
                },
                {
                    'key': 'wants_slow_paced',
                    'text': 'Хотите неспешное, атмосферное кино?',
                    'type': 'yes_no',
                    'explanation': 'Медленное развитие сюжета, глубокое погружение'
                },
                {
                    'key': 'energy_intensity',
                    'text': 'Насколько интенсивный фильм вы готовы смотреть?',
                    'type': 'multiple_choice',
                    'options': ["очень спокойный", "умеренный", "энергичный", "очень интенсивный"]
                },
                {
                    'key': 'wants_visual_spectacle',
                    'text': 'Важны ли для вас визуальные эффекты и экшн-сцены?',
                    'type': 'yes_no',
                    'explanation': 'Зрелищные фильмы с эффектными сценами'
                }
            ],
            'genre': [
                {
                    'key': 'likes_sci_fi',
                    'text': 'Нравится научная фантастика?',
                    'type': 'yes_no'
                },
                {
                    'key': 'likes_drama',
                    'text': 'Нравится драма?',
                    'type': 'yes_no'
                },
                {
                    'key': 'likes_thriller',
                    'text': 'Нравится триллер?',
                    'type': 'yes_no'
                },
                {
                    'key': 'likes_comedy',
                    'text': 'Нравится комедия?',
                    'type': 'yes_no'
                },
                {
                    'key': 'likes_romance',
                    'text': 'Нравится романтика?',
                    'type': 'yes_no'
                },
                {
                    'key': 'likes_fantasy',
                    'text': 'Нравится фэнтези?',
                    'type': 'yes_no'
                },
                {
                    'key': 'likes_adventure',
                    'text': 'Нравится приключения?',
                    'type': 'yes_no'
                },
                {
                    'key': 'likes_horror',
                    'text': 'Нравится хоррор?',
                    'type': 'yes_no'
                },
                {
                    'key': 'likes_mystery',
                    'text': 'Нравится детектив/мистика?',
                    'type': 'yes_no'
                },
                {
                    'key': 'likes_action',
                    'text': 'Нравится боевик?',
                    'type': 'yes_no'
                },
                {
                    'key': 'primary_genre',
                    'text': 'Какой жанр для вас самый важный?',
                    'type': 'multiple_choice',
                    'options': ["научная фантастика", "драма", "триллер", "комедия", "романтика", 
                                "фэнтези", "приключения", "хоррор", "детектив/мистика", "боевик", "другой"]
                }
            ],
            'parameters': [
                {
                    'key': 'wants_plot_twist',
                    'text': 'Важен ли неожиданный поворот сюжета?',
                    'type': 'yes_no',
                    'explanation': 'Фильмы с неожиданной развязкой'
                },
                {
                    'key': 'wants_philosophical',
                    'text': 'Хотите философский подтекст?',
                    'type': 'yes_no',
                    'explanation': 'Фильмы, поднимающие глубокие вопросы'
                },
                {
                    'key': 'wants_complex_plot',
                    'text': 'Предпочитаете сложный, многослойный сюжет?',
                    'type': 'yes_no',
                    'explanation': 'Фильмы, где нужно следить за деталями'
                },
                {
                    'key': 'wants_happy_ending',
                    'text': 'Нужен ли хэппи-энд?',
                    'type': 'yes_no'
                },
                {
                    'key': 'wants_emotional_depth',
                    'text': 'Важна ли эмоциональная глубина?',
                    'type': 'yes_no',
                    'explanation': 'Фильмы, которые трогают до слёз'
                }
            ],
            'context': [
                {
                    'key': 'viewing_company',
                    'text': 'С кем будете смотреть?',
                    'type': 'multiple_choice',
                    'options': ["один", "с партнёром", "с друзьями", "с семьёй", "с детьми"]
                },
                {
                    'key': 'viewing_time',
                    'text': 'Когда планируете смотреть?',
                    'type': 'multiple_choice',
                    'options': ["утро", "день", "вечер", "ночь", "не важно"]
                },
                {
                    'key': 'viewing_purpose',
                    'text': 'Какова цель просмотра?',
                    'type': 'multiple_choice',
                    'options': ["развлечение", "расслабление", "вдохновение", 
                            "интеллектуальное развитие", "эмоциональная встряска"]
                },
                {
                    'key': 'can_focus',
                    'text': 'Готовы уделить фильму полное внимание?',
                    'type': 'yes_no',
                    'explanation': 'Или хотите что-то фоном?'
                }
            ],
            'details': [
                {
                    'key': 'preferred_duration',
                    'text': 'Какую продолжительность предпочитаете?',
                    'type': 'multiple_choice',
                    'options': ["до 90 минут", "90-120 минут", "120-150 минут", 
                            "более 150 минут", "не важно"]
                },
                {
                    'key': 'wants_high_rating',
                    'text': 'Важен ли высокий рейтинг фильма (IMDb/Kinopoisk)?',
                    'type': 'yes_no'
                },
                {
                    'key': 'prefers_recent',
                    'text': 'Интересуют ли современные фильмы (после 2010)?',
                    'type': 'yes_no'
                },
                {
                    'key': 'has_director_preference',
                    'text': 'Хотите фильм определённого режиссёра?',
                    'type': 'yes_no'
                }
            ],
            'final': [
                {
                    'key': 'accepts_foreign_language',
                    'text': 'Готовы смотреть фильмы на иностранном языке?',
                    'type': 'yes_no'
                },
                {
                    'key': 'accepts_classic',
                    'text': 'Интересуют ли культовые/классические фильмы?',
                    'type': 'yes_no'
                },
                {
                    'key': 'accepts_arthouse',
                    'text': 'Принимаете экспериментальное/артхаусное кино?',
                    'type': 'yes_no'
                }
            ]
        }

    def create_session(self):
        session_id = str(uuid.uuid4())
        
        engine = MovieEngine()
        engine.reset()
        
        for film in self.all_films:
            engine.declare(Film(**film))
        
        self.sessions[session_id] = {
            'engine': engine,
            'user_preferences': {},
            'current_stage': 'start',
            'question_history': [],
            'skipped_questions': [],
            'understanding_level': 0.0,
            'answered_questions': 0,
            'consistent_answers': 0,
            'timestamp': datetime.now().isoformat()
        }
        
        return session_id
    
    def process_answer(self, session_id, question_key, answer_value):
        #Обработка ответа пользователя
        if session_id not in self.sessions:
            return {
                'error': 'Сессия не найдена',
                'status': 'error'
            }
        
        session = self.sessions[session_id]
        engine = session['engine']
        
        if isinstance(answer_value, str):
            answer_lower = answer_value.lower()
            if answer_lower in ['да', 'д', 'yes', 'y', '+']:
                answer_value = True
            elif answer_lower in ['нет', 'н', 'no', 'n', '-']:
                answer_value = False
        
        session['user_preferences'][question_key] = answer_value
        
        try:
            facts_to_retract = []
            for fact_id, fact in engine.facts.items():
                if isinstance(fact, Answer) and fact['name'] == question_key:
                    facts_to_retract.append(fact_id)
            
            for fact_id in facts_to_retract:
                engine.retract(fact_id)
            
            #новый факт ответа
            engine.declare(Answer(name=question_key, value=answer_value))
            
            #движок для активации правил
            engine.run(steps=5)
            
            #обновляем уровень понимания
            self.update_understanding(session, question_key, answer_value)
            
            #следующий вопрос
            return self.get_next_question(session_id)
        except Exception as e:
            return {
                'error': f'Ошибка обработки ответа: {str(e)}',
                'status': 'error'
            }
    
    def update_understanding(self, session, question_key, answer_value):
        #счетчик отвеченных вопросов
        session['answered_questions'] += 1
        
        #общее количество вопросов в системе
        total_questions_in_system = 0
        for stage, questions in self.stage_questions.items():
            total_questions_in_system += len(questions)
        
        #процент отвеченных от общего числа
        if total_questions_in_system > 0:
            base_understanding = (session['answered_questions'] / total_questions_in_system) * 100
        else:
            base_understanding = 0
        
        #логическая согласованность
        consistency_score = self.check_consistency(session, question_key, answer_value)
        
        #Важные факторы для понимания
        understanding_factors = {
            'base_progress': base_understanding * 0.4,          
            # 40% - базовый прогресс
            'consistency': consistency_score * 30,              
            # 30% - согласованность ответов
            'stage_completion': 0,                              
            # 20% - завершение стадий
            'diversity': 0,                                    
            # 10% - разнообразие ответов
        }
        
        #завершение стадий
        current_stage = session.get('current_stage', 'start')
        stage_order = ['start', 'energy', 'genre', 'parameters', 'context', 'details', 'final']
        stage_index = stage_order.index(current_stage) if current_stage in stage_order else 0
        stage_completion_percentage = (stage_index / len(stage_order)) * 100
        understanding_factors['stage_completion'] = stage_completion_percentage * 0.2
        
        #разнообразие ответов
        user_prefs = session['user_preferences']
        diversity_score = 0
        if len(user_prefs) > 0:
            #разнообразие типов ответов
            yes_count = sum(1 for v in user_prefs.values() if v is True)
            no_count = sum(1 for v in user_prefs.values() if v is False)
            string_count = sum(1 for v in user_prefs.values() if isinstance(v, str))
            
            #баланс ответов
            total = yes_count + no_count + string_count
            if total > 0:
                max_score = 3
                actual_score = (1 if yes_count > 0 else 0) + (1 if no_count > 0 else 0) + (1 if string_count > 0 else 0)
                diversity_score = (actual_score / max_score) * 100
        understanding_factors['diversity'] = diversity_score * 0.1
        
        #итоговый уровень понимания
        total_understanding = sum(understanding_factors.values())
        
        #бонус за высокую согласованность
        if session['consistent_answers'] > 5:
            consistency_bonus = min(10, (session['consistent_answers'] - 5) * 2)
            total_understanding += consistency_bonus
        
        #штраф за много пропущенных вопросов
        skipped_questions = session.get('skipped_questions', [])
        if len(skipped_questions) > 3:
            skip_penalty = min(20, (len(skipped_questions) - 3) * 5)
            total_understanding = max(0, total_understanding - skip_penalty)
        
        session['understanding_level'] = max(0, min(100, total_understanding))
        
        print(f"DEBUG Понимание: {session['understanding_level']:.1f}%")
        print(f"  - Базовый прогресс: {base_understanding:.1f}%")
        print(f"  - Согласованность: {consistency_score:.2f} ({session['consistent_answers']} совпад.)")
        print(f"  - Завершение стадий: {stage_completion_percentage:.1f}%")
        print(f"  - Разнообразие: {diversity_score:.1f}%")
        print(f"  - Отвечено: {session['answered_questions']}/{total_questions_in_system}")
    
    def check_consistency(self, session, question_key, answer_value):
        #согласованность ответа с предыдущими
        if session['answered_questions'] <= 1:
            return 0.5
        
        user_prefs = session['user_preferences']
        consistency_score = 0.5
        
        #логические правила для оценки согласованности
        consistency_rules = [
            #противоречия в настроении
            {
                'condition': question_key == 'wants_positive_mood' and answer_value == True and 
                            user_prefs.get('wants_tension', False) == True,
                'adjustment': -0.3,
                'reason': 'Трудно совместить позитив и напряжение'
            },
            {
                'condition': question_key == 'wants_tension' and answer_value == True and 
                            user_prefs.get('wants_positive_mood', False) == True,
                'adjustment': -0.3,
                'reason': 'Трудно совместить напряжение и позитив'
            },
            
            #согласованность жанров и настроения
            {
                'condition': question_key == 'likes_horror' and answer_value == True and 
                            user_prefs.get('current_emotion') == 'радость',
                'adjustment': -0.2,
                'reason': 'Хоррор обычно не смотрят в радостном настроении'
            },
            {
                'condition': question_key == 'likes_comedy' and answer_value == True and 
                            user_prefs.get('current_emotion') == 'грусть',
                'adjustment': +0.3,
                'reason': 'Комедии хорошо поднимают настроение'
            },
            
            #согласованность темпа
            {
                'condition': question_key == 'wants_fast_paced' and answer_value == True and 
                            user_prefs.get('wants_slow_paced', False) == True,
                'adjustment': -0.4,
                'reason': 'Противоречие в темпе'
            },
            {
                'condition': question_key == 'wants_slow_paced' and answer_value == True and 
                            user_prefs.get('wants_fast_paced', False) == True,
                'adjustment': -0.4,
                'reason': 'Противоречие в темпе'
            },
            
            #согласованность с целью просмотра
            {
                'condition': question_key == 'wants_thoughtful' and answer_value == True and 
                            user_prefs.get('viewing_purpose') == 'расслабление',
                'adjustment': -0.2,
                'reason': 'Фильмы для размышлений не всегда расслабляют'
            },
            {
                'condition': question_key == 'wants_complex_plot' and answer_value == True and 
                            user_prefs.get('can_focus', True) == False,
                'adjustment': -0.3,
                'reason': 'Сложный сюжет требует внимания'
            },
            
            #согласованность с компанией
            {
                'condition': question_key == 'likes_romance' and answer_value == True and 
                            user_prefs.get('viewing_company') == 'с друзьями',
                'adjustment': -0.1,
                'reason': 'Романтику обычно смотрят вдвоём'
            },
            
            #положительная согласованность
            {
                'condition': question_key == 'wants_visual_spectacle' and answer_value == True and 
                            user_prefs.get('wants_fast_paced', False) == True,
                'adjustment': +0.2,
                'reason': 'Визуальные эффекты хорошо сочетаются с динамикой'
            },
            {
                'condition': question_key == 'wants_philosophical' and answer_value == True and 
                            user_prefs.get('wants_thoughtful', False) == True,
                'adjustment': +0.3,
                'reason': 'Философский подтекст предполагает размышления'
            },
        ]
        
        for rule in consistency_rules:
            if rule['condition']:
                consistency_score += rule['adjustment']
                print(f"  - Согласованность: {rule['reason']} ({rule['adjustment']:+.1f})")
        
        #обновляем счетчик согласованных ответов
        if consistency_score > 0.7:
            session['consistent_answers'] += 2  
            print("  - Высокая согласованность ответа!")
        elif consistency_score > 0.6:
            session['consistent_answers'] += 1
        elif consistency_score < 0.4:
            session['consistent_answers'] = max(0, session['consistent_answers'] - 1)
            print("  - Низкая согласованность ответа")
        
        return min(1.0, max(0.0, consistency_score))
    
    def get_next_question(self, session_id):
        #следующий вопрос на основе текущей стадии
        if session_id not in self.sessions:
            return {
                'error': 'Сессия не найдена',
                'status': 'error'
            }
        
        session = self.sessions[session_id]
        engine = session['engine']
        
        try:
            #движок для активации правил и переходов
            engine.run(steps=10)
            
            #определяем текущую стадию
            current_stage = self.get_current_stage(engine)
            session['current_stage'] = current_stage
            
            print(f"DEBUG: Текущая стадия после запуска движка: {current_stage}")
            print(f"DEBUG: Ответы пользователя: {session['user_preferences'].keys()}")
            
            return self.generate_question(current_stage, session, session_id)
        except Exception as e:
            import traceback
            print(f"ERROR в get_next_question: {str(e)}")
            print(traceback.format_exc())
            return {
                'error': f'Ошибка получения вопроса: {str(e)}',
                'status': 'error'
            }
        
    def get_current_stage(self, engine):
        #Получаем текущую стадию из движка
        for fact_id, fact in engine.facts.items():
            if isinstance(fact, Stage):
                return fact['name']
        return 'start'
    
    def generate_question(self, stage, session, session_id=None):
        #Генерируем вопрос для текущей стадии
        stage_questions = {
            'start': [
                {
                    'key': 'wants_thoughtful',
                    'text': 'Хотите фильм, который заставит задуматься?',
                    'type': 'yes_no',
                    'explanation': 'Интеллектуальные фильмы, поднимающие важные вопросы'
                },
                {
                    'key': 'wants_positive_mood',
                    'text': 'Нужен фильм для поднятия настроения?',
                    'type': 'yes_no',
                    'explanation': 'Фильмы, которые дарят радость и вдохновение'
                },
                {
                    'key': 'wants_tension',
                    'text': 'Хотите почувствовать напряжение и адреналин?',
                    'type': 'yes_no',
                    'explanation': 'Триллеры, хорроры, напряжённые драмы'
                },
                {
                    'key': 'current_emotion',
                    'text': 'Какая эмоция вам ближе сейчас?',
                    'type': 'multiple_choice',
                    'options': ["радость", "грусть", "тревога", "спокойствие", "вдохновение", "любовь"]
                }
            ],
            'energy': [
                {
                    'key': 'wants_fast_paced',
                    'text': 'Предпочитаете быстрый, динамичный темп?',
                    'type': 'yes_no',
                    'explanation': 'Быстрые монтажные склейки, много действий'
                },
                {
                    'key': 'wants_slow_paced',
                    'text': 'Хотите неспешное, атмосферное кино?',
                    'type': 'yes_no',
                    'explanation': 'Медленное развитие сюжета, глубокое погружение'
                },
                {
                    'key': 'energy_intensity',
                    'text': 'Насколько интенсивный фильм вы готовы смотреть?',
                    'type': 'multiple_choice',
                    'options': ["очень спокойный", "умеренный", "энергичный", "очень интенсивный"]
                },
                {
                    'key': 'wants_visual_spectacle',
                    'text': 'Важны ли для вас визуальные эффекты и экшн-сцены?',
                    'type': 'yes_no',
                    'explanation': 'Зрелищные фильмы с эффектными сценами'
                }
            ],
            'genre': [
                {
                    'key': 'likes_sci_fi',
                    'text': 'Нравится научная фантастика?',
                    'type': 'yes_no'
                },
                {
                    'key': 'likes_drama',
                    'text': 'Нравится драма?',
                    'type': 'yes_no'
                },
                {
                    'key': 'likes_thriller',
                    'text': 'Нравится триллер?',
                    'type': 'yes_no'
                },
                {
                    'key': 'likes_comedy',
                    'text': 'Нравится комедия?',
                    'type': 'yes_no'
                },
                {
                    'key': 'likes_romance',
                    'text': 'Нравится романтика?',
                    'type': 'yes_no'
                },
                {
                    'key': 'likes_fantasy',
                    'text': 'Нравится фэнтези?',
                    'type': 'yes_no'
                },
                {
                    'key': 'likes_adventure',
                    'text': 'Нравится приключения?',
                    'type': 'yes_no'
                },
                {
                    'key': 'likes_horror',
                    'text': 'Нравится хоррор?',
                    'type': 'yes_no'
                },
                {
                    'key': 'likes_mystery',
                    'text': 'Нравится детектив/мистика?',
                    'type': 'yes_no'
                },
                {
                    'key': 'likes_action',
                    'text': 'Нравится боевик?',
                    'type': 'yes_no'
                },
                {
                    'key': 'primary_genre',
                    'text': 'Какой жанр для вас самый важный?',
                    'type': 'multiple_choice',
                    'options': ["научная фантастика", "драма", "триллер", "комедия", "романтика", 
                            "фэнтези", "приключения", "хоррор", "детектив/мистика", "боевик", "другой"]
                }
            ],
            'parameters': [
                {
                    'key': 'wants_plot_twist',
                    'text': 'Важен ли неожиданный поворот сюжета?',
                    'type': 'yes_no',
                    'explanation': 'Фильмы с неожиданной развязкой'
                },
                {
                    'key': 'wants_philosophical',
                    'text': 'Хотите философский подтекст?',
                    'type': 'yes_no',
                    'explanation': 'Фильмы, поднимающие глубокие вопросы'
                },
                {
                    'key': 'wants_complex_plot',
                    'text': 'Предпочитаете сложный, многослойный сюжет?',
                    'type': 'yes_no',
                    'explanation': 'Фильмы, где нужно следить за деталями'
                },
                {
                    'key': 'wants_happy_ending',
                    'text': 'Нужен ли хэппи-энд?',
                    'type': 'yes_no'
                },
                {
                    'key': 'wants_emotional_depth',
                    'text': 'Важна ли эмоциональная глубина?',
                    'type': 'yes_no',
                    'explanation': 'Фильмы, которые трогают до слёз'
                }
            ],
            'context': [
                {
                    'key': 'viewing_company',
                    'text': 'С кем будете смотреть?',
                    'type': 'multiple_choice',
                    'options': ["один", "с партнёром", "с друзьями", "с семьёй", "с детьми"]
                },
                {
                    'key': 'viewing_time',
                    'text': 'Когда планируете смотреть?',
                    'type': 'multiple_choice',
                    'options': ["утро", "день", "вечер", "ночь", "не важно"]
                },
                {
                    'key': 'viewing_purpose',
                    'text': 'Какова цель просмотра?',
                    'type': 'multiple_choice',
                    'options': ["развлечение", "расслабление", "вдохновение", 
                            "интеллектуальное развитие", "эмоциональная встряска"]
                },
                {
                    'key': 'can_focus',
                    'text': 'Готовы уделить фильму полное внимание?',
                    'type': 'yes_no',
                    'explanation': 'Или хотите что-то фоном?'
                }
            ],
            'details': [
                {
                    'key': 'preferred_duration',
                    'text': 'Какую продолжительность предпочитаете?',
                    'type': 'multiple_choice',
                    'options': ["до 90 минут", "90-120 минут", "120-150 минут", 
                            "более 150 минут", "не важно"]
                },
                {
                    'key': 'wants_high_rating',
                    'text': 'Важен ли высокий рейтинг фильма (IMDb/Kinopoisk)?',
                    'type': 'yes_no'
                },
                {
                    'key': 'prefers_recent',
                    'text': 'Интересуют ли современные фильмы (после 2010)?',
                    'type': 'yes_no'
                },
                {
                    'key': 'has_director_preference',
                    'text': 'Хотите фильм определённого режиссёра?',
                    'type': 'yes_no'
                }
            ],
            'final': [
                {
                    'key': 'accepts_foreign_language',
                    'text': 'Готовы смотреть фильмы на иностранном языке?',
                    'type': 'yes_no'
                },
                {
                    'key': 'accepts_classic',
                    'text': 'Интересуют ли культовые/классические фильмы?',
                    'type': 'yes_no'
                },
                {
                    'key': 'accepts_arthouse',
                    'text': 'Принимаете экспериментальное/артхаусное кино?',
                    'type': 'yes_no'
                }
            ]
        }
        
        if stage not in stage_questions or stage == 'inference':
            if session_id:
                return self.get_recommendations(session_id)
            else:
                return {
                    'error': 'Session ID не определен',
                    'status': 'error'
                }
        
        questions = stage_questions[stage]
        
        for question in questions:
            question_key = question['key']
            
            if question_key in session['user_preferences']:
                continue
            
            #можно ли пропустить вопрос по логике
            should_skip = self.should_skip_question_logic(question_key, session['user_preferences'])
            if should_skip:
                print(f"DEBUG: Автоматический пропуск вопроса {question_key}")
                default_value = self.get_skipped_value(question_key, question.get('type'), 
                                                    question.get('options', []), 
                                                    session['user_preferences'])
                session['user_preferences'][question_key] = default_value
                
                if session['engine']:
                    session['engine'].declare(Answer(name=question_key, value=default_value))
                    session['engine'].run(steps=1)
                
                self.update_understanding(session, question_key, default_value)
                
                continue
            
            return {
                'session_id': session_id,
                'stage': stage.capitalize(),
                'stage_key': stage,
                'question': question['text'],
                'question_key': question_key,
                'type': question['type'],
                'options': question.get('options', []),
                'explanation': question.get('explanation', ''),
                'progress': self.calculate_progress(session),
                'understanding_level': int(session['understanding_level']),
                'answered_questions': session['answered_questions'],
                'consistent_answers': session['consistent_answers'],
                'can_skip': True
            }
        
        print(f"DEBUG: Все вопросы стадии {stage} отвечены, переход к следующей")
        return self.advance_to_next_stage(session_id, session, stage)

    def should_skip_question_logic(self, question_key, user_prefs):
        #логика пропуска вопросов
        
        skip_logic = {
            # ============ СТАДИЯ 1: НАСТРОЕНИЕ ============
            'wants_positive_mood': (
                user_prefs.get('wants_thoughtful', False) and 
                not user_prefs.get('wants_tension', False)
            ),
            'wants_tension': (
                not user_prefs.get('wants_thoughtful', False) and 
                user_prefs.get('wants_positive_mood', False)
            ),
            'current_emotion': (
                'wants_thoughtful' in user_prefs and 
                'wants_positive_mood' in user_prefs and 
                'wants_tension' in user_prefs
            ),
            
            # ============ СТАДИЯ 2: ЭНЕРГИЯ ============
            'wants_fast_paced': (
                user_prefs.get('wants_tension', False) or 
                user_prefs.get('energy_intensity') == 'энергичный'
            ),
            'wants_slow_paced': (
                not user_prefs.get('wants_fast_paced', False) and 
                user_prefs.get('energy_intensity') == 'очень спокойный'
            ),
            'energy_intensity': (
                'wants_fast_paced' in user_prefs and 
                'wants_slow_paced' in user_prefs
            ),
            'wants_visual_spectacle': (
                user_prefs.get('wants_fast_paced', False) and 
                user_prefs.get('energy_intensity') == 'энергичный'
            ),
            
            # ============ СТАДИЯ 3: ЖАНР ============
            'likes_horror': (
                user_prefs.get('wants_positive_mood', False) and
                user_prefs.get('wants_positive_mood') is True
            ),
            'likes_comedy': (
                user_prefs.get('wants_tension', False) and 
                user_prefs.get('wants_tension') is True and
                not user_prefs.get('wants_positive_mood', False)
            ),
            'primary_genre': (
                'likes_sci_fi' in user_prefs or 
                'likes_drama' in user_prefs or 
                'likes_thriller' in user_prefs or
                'likes_comedy' in user_prefs or
                'likes_romance' in user_prefs or
                'likes_fantasy' in user_prefs or
                'likes_adventure' in user_prefs or
                'likes_horror' in user_prefs or
                'likes_mystery' in user_prefs or
                'likes_action' in user_prefs
            ),
            
            # ============ СТАДИЯ 4: ПАРАМЕТРЫ ============
            'wants_plot_twist': (
                user_prefs.get('wants_complex_plot', False) or
                user_prefs.get('wants_thoughtful', False)
            ),
            'wants_philosophical': (
                user_prefs.get('wants_thoughtful', False) and 
                user_prefs.get('primary_genre') == 'драма'
            ),
            'wants_complex_plot': (
                user_prefs.get('wants_thoughtful', False) and 
                not user_prefs.get('likes_comedy', False)
            ),
            'wants_happy_ending': (
                user_prefs.get('current_emotion') == 'радость' or
                user_prefs.get('viewing_purpose') == 'развлечение'
            ),
            'wants_emotional_depth': (
                user_prefs.get('current_emotion') == 'грусть' or
                user_prefs.get('primary_genre') == 'драма'
            ),
            
            # ============ СТАДИЯ 5: КОНТЕКСТ ============
            'viewing_company': (
                user_prefs.get('likes_comedy', False)
            ),
            'viewing_purpose': (
                'wants_thoughtful' in user_prefs and 
                'wants_positive_mood' in user_prefs
            ),
            'can_focus': (
                user_prefs.get('viewing_purpose') == 'расслабление' or
                user_prefs.get('wants_complex_plot', False)
            ),
            
            # ============ СТАДИЯ 6: ДЕТАЛИ ============
            'has_director_preference': (
                user_prefs.get('prefers_recent', False)
            ),
            
            # ============ СТАДИЯ 7: ФИНАЛЬНЫЕ ПРЕДПОЧТЕНИЯ ============
            'accepts_foreign_language': (
                user_prefs.get('primary_genre') == 'аниме'
            ),
            'accepts_classic': (
                user_prefs.get('prefers_recent', False) and 
                user_prefs.get('prefers_recent') is True
            ),
            'accepts_arthouse': (
                user_prefs.get('wants_visual_spectacle', False) and 
                user_prefs.get('wants_fast_paced', False)
            ),
            
            # ============ ДОПОЛНИТЕЛЬНЫЕ УСЛОВИЯ ============
            'wants_positive_mood_complex': (
                (user_prefs.get('wants_thoughtful', False) and 
                not user_prefs.get('wants_tension', False)) or
                (user_prefs.get('current_emotion') == 'радость' or
                not user_prefs.get('wants_tension', False))
            ),
            
            'wants_tension_complex': (
                (not user_prefs.get('wants_thoughtful', False) and 
                user_prefs.get('wants_positive_mood', False)) or
                (user_prefs.get('current_emotion') == 'тревога' or
                user_prefs.get('wants_visual_spectacle', False))
            ),
            
            'wants_fast_paced_complex': (
                (user_prefs.get('wants_tension', False) or 
                user_prefs.get('energy_intensity') == 'энергичный') or
                (user_prefs.get('wants_visual_spectacle', False) and 
                user_prefs.get('energy_intensity') == 'энергичный')
            ),
            
            'wants_slow_paced_complex': (
                (not user_prefs.get('wants_fast_paced', False) and 
                user_prefs.get('energy_intensity') == 'очень спокойный') or
                (user_prefs.get('current_emotion') == 'спокойствие')
            ),
            
            'wants_visual_spectacle_complex': (
                (user_prefs.get('wants_fast_paced', False) and 
                user_prefs.get('energy_intensity') == 'энергичный') or
                (user_prefs.get('energy_intensity') == 'очень интенсивный' and
                user_prefs.get('wants_fast_paced', False))
            ),
            
            'wants_plot_twist_complex': (
                (user_prefs.get('wants_complex_plot', False) or 
                user_prefs.get('wants_thoughtful', False)) or
                (user_prefs.get('wants_thoughtful', False) and
                user_prefs.get('wants_complex_plot', False))
            ),
            
            'wants_philosophical_complex': (
                (user_prefs.get('wants_thoughtful', False) and 
                user_prefs.get('primary_genre') == 'драма') or
                (user_prefs.get('wants_thoughtful', False) and
                user_prefs.get('current_emotion') == 'вдохновение')
            ),
            
            'wants_complex_plot_complex': (
                (user_prefs.get('wants_thoughtful', False) and 
                not user_prefs.get('likes_comedy', False)) or
                (user_prefs.get('wants_thoughtful', False) and
                user_prefs.get('current_emotion') == 'вдохновение')
            ),
            
            'wants_happy_ending_complex': (
                (user_prefs.get('current_emotion') == 'радость' or
                user_prefs.get('viewing_purpose') == 'развлечение') or
                (user_prefs.get('current_emotion') == 'радость' and
                user_prefs.get('wants_positive_mood', False))
            ),
            
            'wants_emotional_depth_complex': (
                (user_prefs.get('current_emotion') == 'грусть' or
                user_prefs.get('primary_genre') == 'драма') or
                (user_prefs.get('current_emotion') == 'грусть' and
                user_prefs.get('wants_thoughtful', False))
            ),
            
            'viewing_purpose_complex': (
                ('wants_thoughtful' in user_prefs and 
                'wants_positive_mood' in user_prefs) or
                (user_prefs.get('wants_thoughtful', False) and
                user_prefs.get('wants_positive_mood', False))
            ),
            
            'can_focus_complex': (
                (user_prefs.get('viewing_purpose') == 'расслабление' or
                user_prefs.get('wants_complex_plot', False)) or
                (user_prefs.get('viewing_purpose') == 'расслабление' and
                not user_prefs.get('wants_thoughtful', False))
            ),
            
            'has_director_preference_complex': (
                (user_prefs.get('prefers_recent', False)) or
                (user_prefs.get('prefers_recent', False) and
                user_prefs.get('wants_visual_spectacle', False))
            ),
            
            'accepts_foreign_language_complex': (
                (user_prefs.get('primary_genre') == 'аниме') or
                (user_prefs.get('primary_genre') == 'аниме' and
                user_prefs.get('accepts_classic', False))
            ),
            
            'accepts_classic_complex': (
                (user_prefs.get('prefers_recent', False) and 
                user_prefs.get('prefers_recent') is True) or
                (user_prefs.get('prefers_recent', False) and
                user_prefs.get('wants_high_rating', False))
            ),
            
            'accepts_arthouse_complex': (
                (user_prefs.get('wants_visual_spectacle', False) and 
                user_prefs.get('wants_fast_paced', False)) or
                (user_prefs.get('wants_visual_spectacle', False) and
                user_prefs.get('energy_intensity') == 'очень интенсивный')
            ),
        }
        
        if question_key in skip_logic:
            result = skip_logic[question_key]
            
            if isinstance(result, bool):
                return result
            
            try:
                return bool(result)
            except:
                return False
        
        complex_key = f"{question_key}_complex"
        if complex_key in skip_logic:
            result = skip_logic[complex_key]
            try:
                return bool(result)
            except:
                return False
        
        complex_conditions = self.evaluate_complex_conditions(question_key, user_prefs)
        if complex_conditions is not None:
            return complex_conditions
        
        return False

    def evaluate_complex_conditions(self, question_key, user_prefs):
        conditions_map = {
            'wants_positive_mood': "wants_thoughtful && !wants_tension",
            'wants_tension': "!wants_thoughtful && wants_positive_mood",
            'wants_fast_paced': "wants_tension || energy_intensity==энергичный",
            'wants_slow_paced': "!wants_fast_paced && energy_intensity==очень спокойный",
            'wants_visual_spectacle': "wants_fast_paced && energy_intensity==энергичный",
            'wants_plot_twist': "wants_complex_plot || wants_thoughtful",
            'wants_philosophical': "wants_thoughtful && primary_genre==драма",
            'wants_complex_plot': "wants_thoughtful && !likes_comedy",
            'wants_happy_ending': "current_emotion==радость || viewing_purpose==развлечение",
            'wants_emotional_depth': "current_emotion==грусть || primary_genre==драма",
            'can_focus': "viewing_purpose==расслабление || wants_complex_plot",
            'has_director_preference': "prefers_recent",
            'accepts_foreign_language': "primary_genre==аниме",
            'accepts_classic': "prefers_recent==true",
            'accepts_arthouse': "wants_visual_spectacle && wants_fast_paced",
            
            'current_emotion': "has_wants_thoughtful && has_wants_positive_mood && has_wants_tension",
            'energy_intensity': "has_wants_fast_paced && has_wants_slow_paced",
            'viewing_company': "likes_comedy",
            'viewing_purpose': "has_wants_thoughtful && has_wants_positive_mood",
            'primary_genre': f"has_{list(self.genre_map.keys())[0]}" if hasattr(self, 'genre_map') else False,
        }
        
        if question_key not in conditions_map:
            return None
        
        condition_str = conditions_map[question_key]
        
        try:
            condition_str = condition_str.replace('&&', ' and ').replace('||', ' or ').replace('!', ' not ')
            
            condition_str = condition_str.replace('has_', "'")
            condition_str = condition_str.replace(' && ', "' in user_prefs and '")
            condition_str = condition_str.replace(' || ', "' in user_prefs or '")
            
            if "' in user_prefs" in condition_str:
                parts = condition_str.split("' in user_prefs")
                condition_str = "' in user_prefs".join([part + "'" if not part.endswith("'") else part for part in parts])
            
            condition_str = condition_str.replace('==', '==')
            
            safe_dict = {'user_prefs': user_prefs}
            
            for key, value in user_prefs.items():
                safe_dict[key] = value
            
            safe_dict.update({'and': lambda x, y: x and y, 
                            'or': lambda x, y: x or y, 
                            'not': lambda x: not x})
            
            try:
                result = eval(condition_str, {"__builtins__": {}}, safe_dict)
                return bool(result)
            except:
                return self.simple_condition_check(condition_str, user_prefs)
                
        except Exception as e:
            print(f"DEBUG: Ошибка оценки условия {question_key}: {str(e)}")
            return False

    def simple_condition_check(self, condition_str, user_prefs):
        if '==' in condition_str:
            parts = condition_str.split('==')
            if len(parts) == 2:
                key = parts[0].strip().replace("'", "").replace('"', '')
                value = parts[1].strip().replace("'", "").replace('"', '')
                
                if key in user_prefs:
                    if value.lower() in ['true', 'yes', 'да']:
                        return user_prefs[key] is True
                    elif value.lower() in ['false', 'no', 'нет']:
                        return user_prefs[key] is False
                    else:
                        return str(user_prefs[key]) == value
        
        elif ' in user_prefs' in condition_str:
            keys = [k.strip().replace("'", "").replace('"', '') 
                    for k in condition_str.split(' in user_prefs') if k.strip()]
            
            if ' and ' in condition_str:
                return all(key in user_prefs for key in keys if key)
            elif ' or ' in condition_str:
                return any(key in user_prefs for key in keys if key)
            else:
                return all(key in user_prefs for key in keys if key)
        
        return False

    def get_skipped_value(self, question_key, question_type, options, user_prefs):        
        #логические выводы для разных типов вопросов
        logic_map = {
            'wants_thoughtful': {
                'conditions': [
                    user_prefs.get('current_emotion') == 'вдохновение',
                    user_prefs.get('current_emotion') == 'грусть'
                ],
                'value': True,
                'default': False
            },
            'wants_positive_mood': {
                'conditions': [
                    user_prefs.get('current_emotion') == 'радость',
                    not user_prefs.get('wants_tension', False)
                ],
                'value': True,
                'default': True
            },
            'wants_tension': {
                'conditions': [
                    user_prefs.get('current_emotion') == 'тревога',
                    user_prefs.get('wants_visual_spectacle', False)
                ],
                'value': True,
                'default': False
            },
            'wants_fast_paced': {
                'conditions': [
                    user_prefs.get('wants_visual_spectacle', False),
                    user_prefs.get('energy_intensity') == 'энергичный'
                ],
                'value': True,
                'default': False
            },
            'wants_slow_paced': {
                'conditions': [
                    not user_prefs.get('wants_fast_paced', False),
                    user_prefs.get('current_emotion') == 'спокойствие'
                ],
                'value': True,
                'default': False
            },
            'wants_visual_spectacle': {
                'conditions': [
                    user_prefs.get('energy_intensity') == 'очень интенсивный',
                    user_prefs.get('wants_fast_paced', False)
                ],
                'value': True,
                'default': False
            },
            'wants_plot_twist': {
                'conditions': [
                    user_prefs.get('wants_complex_plot', False),
                    user_prefs.get('wants_thoughtful', False)
                ],
                'value': True,
                'default': False
            },
            'wants_philosophical': {
                'conditions': [
                    user_prefs.get('wants_thoughtful', False),
                    user_prefs.get('primary_genre') == 'драма'
                ],
                'value': True,
                'default': False
            },
            'wants_complex_plot': {
                'conditions': [
                    user_prefs.get('wants_thoughtful', False),
                    not user_prefs.get('likes_comedy', False)
                ],
                'value': True,
                'default': False
            },
            'wants_happy_ending': {
                'conditions': [
                    user_prefs.get('current_emotion') == 'радость',
                    user_prefs.get('viewing_purpose') == 'развлечение'
                ],
                'value': True,
                'default': False
            },
            'wants_emotional_depth': {
                'conditions': [
                    user_prefs.get('current_emotion') == 'грусть',
                    user_prefs.get('primary_genre') == 'драма'
                ],
                'value': True,
                'default': False
            },
            
            'current_emotion': {
                'conditions': [
                    user_prefs.get('wants_positive_mood', False),
                    user_prefs.get('wants_tension', False),
                    user_prefs.get('wants_thoughtful', False)
                ],
                'values': ['радость', 'тревога', 'вдохновение'],
                'default': 'радость'
            },
            'energy_intensity': {
                'conditions': [
                    user_prefs.get('wants_fast_paced', False),
                    user_prefs.get('wants_slow_paced', False)
                ],
                'values': ['энергичный', 'умеренный'],
                'default': 'умеренный'
            },
            'viewing_company': {
                'conditions': [
                    user_prefs.get('likes_comedy', False)
                ],
                'values': ['с друзьями', 'один'],
                'default': 'один'
            },
            'viewing_time': {
                'conditions': [],
                'values': ['вечер'],
                'default': 'вечер'
            },
            'viewing_purpose': {
                'conditions': [
                    user_prefs.get('wants_thoughtful', False),
                    user_prefs.get('wants_positive_mood', False)
                ],
                'values': ['интеллектуальное развитие', 'развлечение'],
                'default': 'развлечение'
            },
            'preferred_duration': {
                'conditions': [],
                'values': ['90-120 минут'],
                'default': '90-120 минут'
            }
        }
        
        if question_type == 'yes_no':
            if question_key in logic_map:
                logic = logic_map[question_key]
                for condition in logic['conditions']:
                    if condition:
                        return logic['value']
                return logic.get('default', False)
            
            defaults = {
                'wants_positive_mood': True,
                'accepts_foreign_language': True,
                'accepts_classic': True,
                'can_focus': True,
            }
            return defaults.get(question_key, False)
        
        elif question_type == 'multiple_choice':
            if question_key in logic_map:
                logic = logic_map[question_key]
                
                for i, condition in enumerate(logic['conditions']):
                    if condition and i < len(logic.get('values', [])):
                        value = logic['values'][i]
                        if value in options:
                            return value
                
                default = logic.get('default', options[0] if options else 'не важно')
                return default if default in options else (options[0] if options else 'не важно')
            
            if question_key == 'primary_genre':
                genre_scores = {}
                genre_map = {
                    'likes_sci_fi': 'научная фантастика',
                    'likes_drama': 'драма',
                    'likes_thriller': 'триллер',
                    'likes_comedy': 'комедия',
                    'likes_romance': 'романтика',
                    'likes_fantasy': 'фэнтези',
                    'likes_adventure': 'приключения',
                    'likes_horror': 'хоррор',
                    'likes_mystery': 'детектив/мистика',
                    'likes_action': 'боевик'
                }
                
                for genre_key, genre_name in genre_map.items():
                    if user_prefs.get(genre_key, False) and genre_name in options:
                        genre_scores[genre_name] = genre_scores.get(genre_name, 0) + 2
                
                emotion = user_prefs.get('current_emotion', '')
                if emotion == 'радость' and 'комедия' in options:
                    genre_scores['комедия'] = genre_scores.get('комедия', 0) + 3
                elif emotion == 'грусть' and 'драма' in options:
                    genre_scores['драма'] = genre_scores.get('драма', 0) + 3
                elif emotion == 'тревога' and 'триллер' in options:
                    genre_scores['триллер'] = genre_scores.get('триллер', 0) + 3
                
                if genre_scores:
                    best_genre = max(genre_scores.items(), key=lambda x: x[1])[0]
                    if best_genre in options:
                        return best_genre
            
            defaults = {
                'preferred_duration': '90-120 минут',
                'energy_intensity': 'умеренный',
                'viewing_time': 'вечер',
                'viewing_purpose': 'развлечение',
                'viewing_company': 'один',
            }
            
            default = defaults.get(question_key, options[0] if options else 'не важно')
            return default if default in options else (options[0] if options else 'не важно')
        
        return None

    def advance_to_next_stage(self, session_id, session, current_stage):
        #Переход к следующей стадии
        stage_order = ['start', 'energy', 'genre', 'parameters', 'context', 'details', 'final', 'inference']
        
        current_index = stage_order.index(current_stage) if current_stage in stage_order else 0
        
        if current_index < len(stage_order) - 1:
            next_stage = stage_order[current_index + 1]
            
            engine = session['engine']
            for fact_id, fact in engine.facts.items():
                if isinstance(fact, Stage):
                    engine.modify(fact, name=next_stage)
                    engine.run(steps=1)
                    break
            
            session['current_stage'] = next_stage
            print(f"DEBUG: Переход от {current_stage} к {next_stage}")
            
            return self.generate_question(next_stage, session, session_id)
        else:
            return self.get_recommendations(session_id)

    def get_next_stage(self, current_stage):
        #Определяем следующую стадию
        stage_order = ['start', 'energy', 'genre', 'parameters', 'context', 'details', 'final']
        try:
            current_index = stage_order.index(current_stage)
            if current_index + 1 < len(stage_order):
                return stage_order[current_index + 1]
            return 'final'
        except ValueError:
            return 'start'
    
    def calculate_progress(self, session):
        #прогресс заполнения динамически
        total_possible_questions = 0
        for stage, questions in self.stage_questions.items():
            total_possible_questions += len(questions)
        
        answered_count = len(session['user_preferences'])
        
        auto_skipped_count = len(session.get('skipped_questions', []))
        total_answered = answered_count + auto_skipped_count
        
        if total_possible_questions > 0:
            progress = (total_answered / total_possible_questions) * 100
        else:
            progress = 0
        
        progress = max(0, min(100, progress))
        
        print(f"DEBUG Прогресс: {total_answered}/{total_possible_questions} = {progress:.1f}%")
        print(f"  - Отвечено вручную: {answered_count}")
        print(f"  - Автопропущено: {auto_skipped_count}")
        print(f"  - Стадия: {session.get('current_stage', 'start')}")
        
        return int(progress)
    
    def get_recommendations(self, session_id):
        #рекомендации фильмов
        session = self.sessions[session_id]
        engine = session['engine']
        user_prefs = session['user_preferences']
        
        engine.declare(Stage(name='inference'))
        engine.run(steps=50)
        
        conditions = []
        activated_rules = {}
        
        for fact in engine.facts.items():
            if isinstance(fact[1], FilterCondition):
                conditions.append(fact[1])
                activated_rules[fact[1]['type']] = True
        
        scored_films = []
        
        for film_data in self.all_films:
            score = 0
            matches = []
            
            genre_map = {
                'likes_sci_fi': 'science fiction',
                'likes_drama': 'drama',
                'likes_thriller': 'thriller',
                'likes_comedy': 'comedy',
            }
            
            for genre_key, target_genre in genre_map.items():
                if user_prefs.get(genre_key, False) and target_genre in film_data['genres']:
                    score += 2
                    matches.append(f"жанр: {target_genre}")
                elif user_prefs.get(genre_key, False) == False and target_genre in film_data['genres']:
                    #Штраф за нежелательный жанр
                    score -= 1  
            
            for condition in conditions:
                cond_type = condition['type']
                
                if cond_type == "thought_provoking" and film_data['features']['is_thought_provoking']:
                    score += condition['weight']
                    matches.append("заставляет думать")
                elif cond_type == "not_thought_provoking" and not film_data['features']['is_thought_provoking']:
                    score += condition['weight']
                    matches.append("не слишком глубокий")
                
                elif cond_type == "tension":
                    tense_moods = ['tense', 'suspenseful', 'dark', 'mysterious', 'intense']
                    for mood in film_data['mood']:
                        if any(tense in mood.lower() for tense in tense_moods):
                            score += condition['weight']
                            matches.append("напряжение")
                            break
                elif cond_type == "not_tension":
                    tense_moods = ['tense', 'suspenseful', 'dark', 'mysterious', 'intense']
                    has_tension = False
                    for mood in film_data['mood']:
                        if any(tense in mood.lower() for tense in tense_moods):
                            has_tension = True
                            break
                    if not has_tension:
                        score += condition['weight']
                        matches.append("без напряжения")
                
                elif cond_type == "fast_paced" and film_data['features']['is_fast_paced']:
                    score += condition['weight']
                    matches.append("динамичный темп")
                elif cond_type == "not_fast_paced" and not film_data['features']['is_fast_paced']:
                    score += condition['weight']
                    matches.append("неспешный темп")
                
                elif cond_type == "has_twist" and film_data['features']['has_plot_twist']:
                    score += condition['weight']
                    matches.append("поворот сюжета")
                elif cond_type == "not_has_twist" and not film_data['features']['has_plot_twist']:
                    score += condition['weight']
                    matches.append("прямолинейный сюжет")
                
                elif cond_type == "philosophical" and film_data['parameters']['philosophical'] > 0.7:
                    score += condition['weight']
                    matches.append("философский")
                elif cond_type == "not_philosophical" and film_data['parameters']['philosophical'] <= 0.3:
                    score += condition['weight']
                    matches.append("не философский")
                
                elif cond_type == "happy_ending" and film_data['features']['has_happy_ending']:
                    score += condition['weight']
                    matches.append("хэппи-энд")
                elif cond_type == "not_happy_ending" and not film_data['features']['has_happy_ending']:
                    score += condition['weight']
                    matches.append("неоднозначная концовка")
                
                elif cond_type == "visual" and film_data['parameters']['visual'] > 0.7:
                    score += condition['weight']
                    matches.append("визуальные эффекты")
                elif cond_type == "not_visual" and film_data['parameters']['visual'] <= 0.3:
                    score += condition['weight']
                    matches.append("минимальные эффекты")
                
                elif cond_type == "complex" and film_data['parameters']['complexity'] > 0.7:
                    score += condition['weight']
                    matches.append("сложный сюжет")
                elif cond_type == "not_complex" and film_data['parameters']['complexity'] <= 0.3:
                    score += condition['weight']
                    matches.append("простой сюжет")
            
            #учет рейтинга
            if user_prefs.get('wants_high_rating', False):
                score += film_data['rating'] / 10
            elif user_prefs.get('wants_high_rating', False) == False:
                score += 0.5
            
            #учет продолжительности
            duration_pref = user_prefs.get('preferred_duration', 'не важно')
            duration = film_data['duration']
            
            if duration_pref == "до 90 минут" and duration <= 90:
                score += 1
            elif duration_pref == "90-120 минут" and 90 < duration <= 120:
                score += 1
            elif duration_pref == "120-150 минут" and 120 < duration <= 150:
                score += 1
            elif duration_pref == "более 150 минут" and duration > 150:
                score += 1
            elif duration_pref == "не важно":
                score += 0.5
            
            score += 0.1
            
            #сохраняем фильм если он набрал баллы
            scored_films.append({
                'film': film_data,
                'score': score,
                'matches': list(set(matches))
            })
        
        scored_films.sort(key=lambda x: x['score'], reverse=True)
        top_films = scored_films[:3]
        
        recommendations = []
        for result in top_films:
            film = result['film']
            recommendations.append({
                'title': film['title'],
                'original_title': film['original_title'],
                'year': film['year'],
                'rating': film['rating'],
                'duration': film['duration'],
                'genres': film['genres'],
                'director': film['director'],
                'description': film['description'],
                'score': round(result['score'], 2),
                'matches': result['matches'][:5],
                'poster': film.get('poster', '')
            })
        
        return {
            'session_id': session_id,
            'status': 'completed',
            'recommendations': recommendations,
            'statistics': {
                'total_films_analyzed': len(self.all_films),
                'matching_films_found': len(scored_films),
                'understanding_level': int(session['understanding_level']),
                'answered_questions': session['answered_questions'],
                'consistent_answers': session['consistent_answers'],
                'activated_rules': len(activated_rules)
            }
        }
    
    def skip_question(self, session_id, question_key):
        #Пропустить вопрос
        if session_id not in self.sessions:
            return {
                'error': 'Сессия не найдена',
                'status': 'error'
            }
        
        session = self.sessions[session_id]
        user_prefs = session['user_preferences']
        
        default_value = self.get_default_value(question_key)
        user_prefs[question_key] = default_value
        
        try:
            session['engine'].declare(Answer(name=question_key, value=default_value))
            
            return self.get_next_question(session_id)
        except Exception as e:
            return {
                'error': f'Ошибка пропуска вопроса: {str(e)}',
                'status': 'error'
            }
    
    def get_default_value(self, key):
        defaults = {
            'wants_positive_mood': True,
            'accepts_foreign_language': True,
            'accepts_classic': True,
            'can_focus': True,
        }
        return defaults.get(key, False)

#Основной логический движок
class MovieEngine(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.filtered_films = []
        self.activated_rules = {}
        self.conditions = []
        self.user_preferences = {}
        self.skipped_questions = {}
        self.question_history = []
        self.understanding_level = 0.0
        self.answered_questions = 0
        self.consistent_answers = 0
    
    @DefFacts()
    def initial_facts(self):
        yield Stage(name="start")
        yield Context(viewing_time="unknown", company="alone", purpose="entertainment")


    @Rule(
        AS.stage << Stage(name='start'),
        AS.answer << Answer(name='current_emotion')
    )
    def transition_to_energy(self, stage, answer):
        self.modify(stage, name='energy')
    
    @Rule(
        AS.stage << Stage(name='energy'),
        AS.answer << Answer(name='wants_visual_spectacle')
    )
    def transition_to_genre(self, stage, answer):
        self.modify(stage, name='genre')
    
    @Rule(
        AS.stage << Stage(name='genre'),
        AS.answer << Answer(name='primary_genre')
    )
    def transition_to_parameters(self, stage, answer):
        self.modify(stage, name='parameters')
    
    @Rule(
        AS.stage << Stage(name='parameters'),
        AS.answer << Answer(name='wants_emotional_depth')
    )
    def transition_to_context(self, stage, answer):
        self.modify(stage, name='context')
    
    @Rule(
        AS.stage << Stage(name='context'),
        AS.answer << Answer(name='can_focus')
    )
    def transition_to_details(self, stage, answer):
        self.modify(stage, name='details')
    
    @Rule(
        AS.stage << Stage(name='details'),
        AS.answer << Answer(name='wants_high_rating')
    )
    def transition_to_final(self, stage, answer):
        self.modify(stage, name='final')
    
    @Rule(
        AS.stage << Stage(name='final'),
        AS.answer << Answer(name='accepts_arthouse')
    )
    def transition_to_inference(self, stage, answer):
        self.modify(stage, name='inference')

    #Правило 1: Настроение -> вдохновение
    @Rule(
        Answer(name='current_emotion', value='вдохновение'),
        salience=10
    )
    def rule_inspiration_mood(self):
        if not self.activated_rules.get('inspiration_mood'):
            self.declare(FilterCondition(type="inspiration_mood", weight=2.0))
            self.activated_rules['inspiration_mood'] = True
            print("   ✅ Правило 1: настроение 'вдохновение' активировано")
    
    #Правило 2: Фильмы для размышления
    @Rule(
        Answer(name='wants_thoughtful', value=True),
        salience=10
    )
    def rule_thoughtful(self):
        if not self.activated_rules.get('thought_provoking'):
            self.declare(FilterCondition(type="thought_provoking", weight=1.8))
            self.activated_rules['thought_provoking'] = True
            print("   ✅ Правило 2: 'хочет задуматься' активировано")
    
    #Правило 3: Напряжение
    @Rule(
        Answer(name='wants_tension', value=True),
        salience=10
    )
    def rule_tension(self):
        if not self.activated_rules.get('tension'):
            self.declare(FilterCondition(type="tension", weight=1.5))
            self.activated_rules['tension'] = True
            print("   ✅ Правило 3: 'хочет напряжения' активировано")
    
    #Правило 4: Динамичные фильмы
    @Rule(
        Answer(name='wants_fast_paced', value=True),
        salience=10
    )
    def rule_fast_paced(self):
        if not self.activated_rules.get('fast_paced'):
            self.declare(FilterCondition(type="fast_paced", weight=1.2))
            self.activated_rules['fast_paced'] = True
            print("   ✅ Правило 4: 'динамичный темп' активировано")
    
    #Правило 5: Фильмы с поворотом сюжета
    @Rule(
        Answer(name='wants_plot_twist', value=True),
        salience=10
    )
    def rule_plot_twist(self):
        if not self.activated_rules.get('has_twist'):
            self.declare(FilterCondition(type="has_twist", weight=1.0))
            self.activated_rules['has_twist'] = True
            print("   ✅ Правило 5: 'поворот сюжета' активировано")
    
    #Правило 6: Философские фильмы
    @Rule(
        Answer(name='wants_philosophical', value=True),
        salience=10
    )
    def rule_philosophical(self):
        if not self.activated_rules.get('philosophical'):
            self.declare(FilterCondition(type="philosophical", weight=1.5))
            self.activated_rules['philosophical'] = True
            print("   ✅ Правило 6: 'философский подтекст' активировано")
    
    #Правило 7: Эмоциональные фильмы
    @Rule(
        Answer(name='wants_emotional_depth', value=True),
        salience=10
    )
    def rule_emotional(self):
        if not self.activated_rules.get('emotional'):
            self.declare(FilterCondition(type="emotional", weight=1.0))
            self.activated_rules['emotional'] = True
            print("   ✅ Правило 7: 'эмоциональная глубина' активировано")
    
    #Правило 8: Визуально эффектные фильмы
    @Rule(
        Answer(name='wants_visual_spectacle', value=True),
        salience=10
    )
    def rule_visual(self):
        if not self.activated_rules.get('visual'):
            self.declare(FilterCondition(type="visual", weight=0.8))
            self.activated_rules['visual'] = True
            print("   ✅ Правило 8: 'визуальные эффекты' активировано")
    
    #Правило 9: Сложный сюжет
    @Rule(
        Answer(name='wants_complex_plot', value=True),
        salience=10
    )
    def rule_complex(self):
        if not self.activated_rules.get('complex'):
            self.declare(FilterCondition(type="complex", weight=1.3))
            self.activated_rules['complex'] = True
            print("   ✅ Правило 9: 'сложный сюжет' активировано")
    
    #Правило 10: Хэппи-энд
    @Rule(
        Answer(name='wants_happy_ending', value=True),
        salience=10
    )
    def rule_happy_ending(self):
        if not self.activated_rules.get('happy_ending'):
            self.declare(FilterCondition(type="happy_ending", weight=1.0))
            self.activated_rules['happy_ending'] = True
            print("   ✅ Правило 10: 'хэппи-энд' активировано")
    
    #Правило 11: Просмотр в одиночку
    @Rule(
        Context(company='один'),
        salience=10
    )
    def rule_solo_viewing(self):
        if not self.activated_rules.get('solo_friendly'):
            self.declare(FilterCondition(type="solo_friendly", weight=0.5))
            self.activated_rules['solo_friendly'] = True
            print("   ✅ Правило 11: 'просмотр в одиночку' активировано")
    
    #Правило 12: Вечерний просмотр
    @Rule(
        Context(viewing_time='вечер'),
        salience=10
    )
    def rule_evening_viewing(self):
        if not self.activated_rules.get('evening_friendly'):
            self.declare(FilterCondition(type="evening_friendly", weight=0.3))
            self.activated_rules['evening_friendly'] = True
            print("   ✅ Правило 12: 'вечерний просмотр' активировано")
    
    #Правило 13: Фильмы для вдохновения (цель просмотра)
    @Rule(
        Context(purpose='вдохновение'),
        salience=10
    )
    def rule_inspiration_purpose(self):
        if not self.activated_rules.get('inspiration_purpose'):
            self.declare(FilterCondition(type="inspiration_purpose", weight=1.2))
            self.activated_rules['inspiration_purpose'] = True
            print("   ✅ Правило 13: 'цель - вдохновение' активировано")
    
    #Правило 14: Позитивное настроение (радость)
    @Rule(
        Answer(name='current_emotion', value='радость'),
        salience=10
    )
    def rule_positive_mood(self):
        if not self.activated_rules.get('positive_mood'):
            self.declare(FilterCondition(type="positive_mood", weight=2.0))
            self.activated_rules['positive_mood'] = True
            print("   ✅ Правило 14: 'позитивное настроение' активировано")

    #Правило 15: Комедийные фильмы
    @Rule(
        Answer(name='primary_genre', value='комедия'),
        salience=10
    )
    def rule_comedy_genre(self):
        if not self.activated_rules.get('comedy_genre'):
            self.declare(FilterCondition(type="comedy_genre", weight=1.5))
            self.activated_rules['comedy_genre'] = True
            print("   ✅ Правило 15: 'комедийный жанр' активировано")

    #Правило 16: Фильмы для развлечения
    @Rule(
        Context(purpose='развлечение'),
        salience=10
    )
    def rule_entertainment_purpose(self):
        if not self.activated_rules.get('entertainment_purpose'):
            self.declare(FilterCondition(type="entertainment_purpose", weight=1.2))
            self.activated_rules['entertainment_purpose'] = True
            print("   ✅ Правило 16: 'цель - развлечение' активировано")

    #Правило 17: Меланхоличное настроение (грусть)
    @Rule(
        Answer(name='current_emotion', value='грусть'),
        salience=10
    )
    def rule_sad_mood(self):
        if not self.activated_rules.get('sad_mood'):
            self.declare(FilterCondition(type="sad_mood", weight=2.0))
            self.activated_rules['sad_mood'] = True
            print("   ✅ Правило 17: 'меланхоличное настроение' активировано")

    #Правило 1a: НЕ хочет фильм для размышления
    @Rule(
        Answer(name='wants_thoughtful', value=False),
        salience=10
    )
    def rule_not_thoughtful(self):
        if not self.activated_rules.get('not_thought_provoking'):
            self.declare(FilterCondition(type="not_thought_provoking", weight=0.5))
            self.activated_rules['not_thought_provoking'] = True
            print("   ✅ Правило 1a: 'НЕ хочет задуматься' активировано")
    
    #Правило 2a: НЕ нужен фильм для поднятия настроения
    @Rule(
        Answer(name='wants_positive_mood', value=False),
        salience=10
    )
    def rule_not_positive_mood(self):
        if not self.activated_rules.get('not_positive_mood'):
            self.declare(FilterCondition(type="not_positive_mood", weight=0.5))
            self.activated_rules['not_positive_mood'] = True
            print("   ✅ Правило 2a: 'НЕ нужен позитивный настрой' активировано")
    
    #Правило 3a: НЕ хочет напряжения
    @Rule(
        Answer(name='wants_tension', value=False),
        salience=10
    )
    def rule_not_tension(self):
        if not self.activated_rules.get('not_tension'):
            self.declare(FilterCondition(type="not_tension", weight=0.5))
            self.activated_rules['not_tension'] = True
            print("   ✅ Правило 3a: 'НЕ хочет напряжения' активировано")
    
    #Правило 4a: НЕ хочет динамичный темп
    @Rule(
        Answer(name='wants_fast_paced', value=False),
        salience=10
    )
    def rule_not_fast_paced(self):
        if not self.activated_rules.get('not_fast_paced'):
            self.declare(FilterCondition(type="not_fast_paced", weight=0.5))
            self.activated_rules['not_fast_paced'] = True
            print("   ✅ Правило 4a: 'НЕ хочет динамичный темп' активировано")
    
    #Правило 5a: НЕ хочет поворот сюжета
    @Rule(
        Answer(name='wants_plot_twist', value=False),
        salience=10
    )
    def rule_not_plot_twist(self):
        if not self.activated_rules.get('not_has_twist'):
            self.declare(FilterCondition(type="not_has_twist", weight=0.5))
            self.activated_rules['not_has_twist'] = True
            print("   ✅ Правило 5a: 'НЕ хочет поворот сюжета' активировано")
    
    #Правило 6a: НЕ хочет философский подтекст
    @Rule(
        Answer(name='wants_philosophical', value=False),
        salience=10
    )
    def rule_not_philosophical(self):
        if not self.activated_rules.get('not_philosophical'):
            self.declare(FilterCondition(type="not_philosophical", weight=0.5))
            self.activated_rules['not_philosophical'] = True
            print("   ✅ Правило 6a: 'НЕ хочет философский подтекст' активировано")
    
    #Правило 9a: НЕ хочет сложный сюжет
    @Rule(
        Answer(name='wants_complex_plot', value=False),
        salience=10
    )
    def rule_not_complex(self):
        if not self.activated_rules.get('not_complex'):
            self.declare(FilterCondition(type="not_complex", weight=0.5))
            self.activated_rules['not_complex'] = True
            print("   ✅ Правило 9a: 'НЕ хочет сложный сюжет' активировано")
    
    #Правило 10a: НЕ нужен хэппи-энд
    @Rule(
        Answer(name='wants_happy_ending', value=False),
        salience=10
    )
    def rule_not_happy_ending(self):
        if not self.activated_rules.get('not_happy_ending'):
            self.declare(FilterCondition(type="not_happy_ending", weight=0.5))
            self.activated_rules['not_happy_ending'] = True
            print("   ✅ Правило 10a: 'НЕ нужен хэппи-энд' активировано")
    
    #Правило 8a: НЕ хочет визуальные эффекты
    @Rule(
        Answer(name='wants_visual_spectacle', value=False),
        salience=10
    )
    def rule_not_visual(self):
        if not self.activated_rules.get('not_visual'):
            self.declare(FilterCondition(type="not_visual", weight=0.5))
            self.activated_rules['not_visual'] = True
            print("   ✅ Правило 8a: 'НЕ хочет визуальные эффекты' активировано")

    @Rule(Stage(name='start'))
    def stage_mood_rule(self):
        pass
    
    @Rule(Stage(name='energy'))
    def stage_energy_rule(self):
        pass
    
    @Rule(Stage(name='genre'))
    def stage_genre_rule(self):
        pass
    
    @Rule(Stage(name='parameters'))
    def stage_parameters_rule(self):
        pass
    
    @Rule(Stage(name='context'))
    def stage_context_rule(self):
        pass
    
    @Rule(Stage(name='details'))
    def stage_details_rule(self):
        pass
    
    @Rule(Stage(name='final'))
    def stage_final_rule(self):
        pass
    
    @Rule(Stage(name='inference'), salience=1000)
    def make_recommendations_rule(self):
        pass

#Иницилизация API
movie_expert = MovieExpertAPI()


@app.route('/api/start', methods=['POST'])
def start_session():
    session_id = movie_expert.create_session()
    return jsonify({
        'success': True,
        'session_id': session_id,
        'message': 'Сессия создана'
    })


@app.route('/api/question', methods=['GET'])
def get_question():
    session_id = request.args.get('session_id')
    if not session_id:
        return jsonify({'error': 'session_id required'}), 400
    
    result = movie_expert.get_next_question(session_id)
    return jsonify(result)

@app.route('/api/answer', methods=['POST'])
def submit_answer():
    try:
        data = request.json
        
        print(f"DEBUG: Получен запрос /api/answer: {json.dumps(data, ensure_ascii=False)}")
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        session_id = data.get('session_id')
        question_key = data.get('question_key')
        answer = data.get('answer')
        
        if not session_id:
            return jsonify({'error': 'Missing session_id'}), 400
        if not question_key:
            return jsonify({'error': 'Missing question_key'}), 400
        if answer is None:
            return jsonify({'error': 'Missing answer'}), 400
        
        print(f"DEBUG: Обработка ответа для {session_id}: {question_key} = {answer}")
        
        result = movie_expert.process_answer(session_id, question_key, answer)
        return jsonify(result)
    except Exception as e:
        print(f"ERROR в submit_answer: {str(e)}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.route('/api/skip', methods=['POST'])
def skip_question():
    data = request.json
    session_id = data.get('session_id')
    question_key = data.get('question_key')
    
    if not all([session_id, question_key]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    result = movie_expert.skip_question(session_id, question_key)
    return jsonify(result)


@app.route('/api/status/<session_id>', methods=['GET'])
def get_status(session_id):
    if session_id not in movie_expert.sessions:
        return jsonify({'error': 'Сессия не найдена'}), 404
    
    session = movie_expert.sessions[session_id]
    return jsonify({
        'session_id': session_id,
        'current_stage': session['current_stage'],
        'answered_questions': session['answered_questions'],
        'understanding_level': int(session['understanding_level']),
        'progress': movie_expert.calculate_progress(session),
        'user_preferences': session['user_preferences']
    })


@app.route('/api/recommendations/<session_id>', methods=['GET'])
def get_recommendations(session_id):
    if session_id not in movie_expert.sessions:
        return jsonify({'error': 'Сессия не найдена'}), 404
    
    result = movie_expert.get_recommendations(session_id)
    return jsonify(result)

@app.route('/api/reset/<session_id>', methods=['POST'])
def reset_session(session_id):
    if session_id in movie_expert.sessions:
        movie_expert.sessions[session_id] = movie_expert.create_new_session(session_id)
        return jsonify({
            'success': True,
            'session_id': session_id,
            'message': 'Сессия сброшена'
        })
    else:
        return jsonify({'error': 'Сессия не найдена'}), 404
    
@app.route('/api/films', methods=['GET'])
def get_all_films():
    return jsonify({
        'films': movie_expert.all_films,
        'count': len(movie_expert.all_films)
    })


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'sessions_active': len(movie_expert.sessions)
    })


if __name__ == '__main__':
    print("Экспертная система подбора фильмов запущена!")
    print("API доступно по адресу: http://localhost:5000")
    app.run(debug=True, port=5000)
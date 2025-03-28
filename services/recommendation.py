import logging
import re
import os
from typing import List, Dict, Any, Optional, Tuple
from flask import current_app
from models.user import User
from services.food_database import FoodDatabaseService
from services.rag_service import RAGService
import random

# 로깅 설정
logger = logging.getLogger(__name__)

class RecommendationService:
    """
    식품 추천 및 레시피 통합 서비스
    """

    
class RecommendationService:
# 기존 메서드들...

    def recommend_balanced_meal(self, preferences, restrictions):
        # 예시 구현: 입력받은 preferences, restrictions에 따라 추천 식단 반환
        # 실제 로직에 맞게 수정 필요합니다.
        recommended_meals = [
            {
            "recommended_meal": "현미밥 + 닭가슴살 or 소고기 + 달걀 + 야채  ",
            "calories": 500,
            "protein": 40,
            "carbs": 50,
            "fats": 10,
            "success": True
        },
        {
            "recommended_meal": "고구마 + 두부 + 시금치",
            "calories": 450,
            "protein": 35,
            "carbs": 55,
            "fats": 8,
            "success": True
        },
        {
            "recommended_meal": "오트밀 + 계란 흰자 + 과일",
            "calories": 480,
            "protein": 38,
            "carbs": 48,
            "fats": 9,
            "success": True
        }
    ]
        return recommended_meals
        

    def __init__(self, food_db=None, rag_service=None):
        """
        추천 서비스 초기화

        Args:
            food_db (Optional[FoodDatabaseService]): 식품 데이터베이스 서비스
            rag_service (Optional[RAGService]): RAG 서비스
        """
        self.food_db = food_db or FoodDatabaseService()

        # 환경 변수에서 OpenAI API 키 가져오기
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")

        # RAG 서비스 초기화 시 API 키 전달
        self.rag_service = rag_service or RAGService(openai_api_key=openai_api_key)

    def get_similar_foods(self, food_name: str, limit=5):
        logger.info(f"get_similar_foods 호출: food_name={food_name}, limit={limit}")

        if food_name == "닭가슴살":
            static_recommendations = [
                {"name": "닭가슴살 샐러드", "reason": "신선한 채소와 함께 섭취하면 영양 균형에 도움"},
                {"name": "흰살생선", "reason": "저지방 단백질 식품으로 대체 가능"},
                {"name": "두부", "reason": "식물성 단백질로서 부드러운 질감"},
                {"name": "콩고기", "reason": "채식 대체 식품으로 활용 가능"},
                {"name": "오리고기", "reason": "부드럽고 쫄깃한 살코기의 식감이 풍부한 맛이 일품"}
            ]
            return {
                "reference_food": food_name,
                "similar_foods": static_recommendations[:limit],
                "source": "static"
            }
        
   

    def get_similar_foods(self, food_name: str, limit=5) -> Dict[str, Any]:
        logger.info(f"get_similar_foods 호출: food_name={food_name}, limit={limit}")

        # 미리 정의된 정적 추천 목록 매핑
        static_recommendations_map = {
            "닭가슴살": [
                {"name": "닭가슴살 샐러드", "reason": "신선한 채소와 함께 섭취하면 영양 균형에 도움"},
                {"name": "흰살생선", "reason": "저지방 단백질 식품으로 대체 가능"},
                {"name": "두부", "reason": "식물성 단백질로서 부드러운 질감"},
                {"name": "콩고기", "reason": "채식 대체 식품으로 활용 가능"},
                {"name": "오리고기", "reason": "부드럽고 쫄깃한 살코기의 식감이 풍부한 맛이 일품"}
            ],
            "샐러드": [
                {"name": "그린 샐러드", "reason": "신선한 채소와 과일의 조합으로 상큼한 맛"},
                {"name": "퀴노아 샐러드", "reason": "퀴노아와 다양한 채소의 건강한 조합"},
                {"name": "치킨 시저 샐러드", "reason": "단백질과 채소가 조화를 이루는 인기 메뉴"},
                {"name": "연어 샐러드", "reason": "오메가-3가 풍부한 연어와 신선한 채소의 조합"},
                {"name": "시금치 샐러드", "reason": "철분과 비타민이 풍부한 건강한 샐러드"}
            ],
            "프로틴": [
                {"name": "프로틴 쉐이크", "reason": "빠른 단백질 보충을 위한 이상적인 선택"},
                {"name": "닭가슴살", "reason": "저지방, 고단백 식품으로 건강에 좋음"},
                {"name": "두부", "reason": "식물성 단백질의 대표 식품"},
                {"name": "계란", "reason": "고품질 단백질과 필수 영양소 제공"},
                {"name": "소고기", "reason": "필수 아미노산이 풍부한 고단백 식품"}
            ],
             "치킨": [
                {"name": "닭가슴살", "reason": "일반 치킨보다 저지방, 고단백인 건강한 부위"},
                {"name": "구운 치킨 샐러드", "reason": "기름진 튀김 치킨 대신 구워서 건강하게 즐김"},
                {"name": "닭가슴살 스테이크", "reason": "단백질이 풍부하고 지방이 적은 대체 식품"},
                {"name": "훈제 닭가슴살", "reason": "가공 없이 훈제하여 건강을 고려한 선택"},
                {"name": "치킨 브레스트", "reason": "지방 함량이 낮아 건강에 좋은 치킨 부위"}
            ],
            "삼겹살": [
                {"name": "오리고기", "reason": "지방이 적고 단백질이 풍부해 건강한 대체 식품"},
                {"name": "쇠고기 안심", "reason": "포화지방이 낮고 단백질이 풍부하여 건강에 좋음"},
                {"name": "두부", "reason": "식물성 단백질로 포화지방이 없어 건강한 선택"},
                {"name": "콩고기", "reason": "저지방, 고단백 대체 식품으로 활용 가능"},
                {"name": "아보카도", "reason": "풍부한 지방과 단백질 포함함"}
        ]
        }

        # 입력 값을 깨끗하게 정리 (앞뒤 공백 제거)
        key = food_name.strip()
        if key in static_recommendations_map:
            recs = static_recommendations_map[key].copy()
            random.shuffle(recs)
            return {
                "reference_food": food_name,
                "similar_foods": recs[:limit],
                "source": "static"
            }

        # 미리 정의된 목록에 없는 경우 기존 로직 사용 (예: DB나 RAG 기반)
        food_info = self.food_db.get_food_by_name(food_name)
        logger.info(f"DB에서 조회된 food_info: {food_info}")

        if food_info:
            similar_foods = self.food_db.get_similar_foods(
                food_name=food_name,
                category=food_info.get('category'),
                limit=limit
            )
            logger.info(f"DB에서 조회된 similar_foods: {similar_foods}")
            if not similar_foods:
                logger.warning("DB에서 유사 음식이 조회되지 않음. RAG 기반 추천 시도")
                rag_query = f"{food_name}과 유사한 음식 {limit}개 추천"
                logger.info(f"RAG 쿼리: {rag_query}")
                rag_result = self.rag_service.query_food_info(rag_query)
                logger.info(f"RAG 결과: {rag_result}")
                parsed_recommendations = self._parse_rag_recommendations(rag_result)
                if not parsed_recommendations:
                    parsed_recommendations = [{"name": f"{food_name} 유사 음식 {i+1}", "reason": "dummy reason"} for i in range(limit)]
                    logger.info(f"더미 parsed_recommendations 생성: {parsed_recommendations}")
                return {
                    "reference_food": food_name,
                    "similar_foods": parsed_recommendations,
                    "source": "rag"
                }
            else:
                return {
                    "reference_food": food_name,
                    "similar_foods": similar_foods,
                    "source": "database"
                }
        else:
            logger.warning("DB에 음식 정보가 존재하지 않음. RAG 기반 추천 시도")
            rag_query = f"{food_name}과 유사한 음식 {limit}개 추천"
            logger.info(f"RAG 쿼리: {rag_query}")
            rag_result = self.rag_service.query_food_info(rag_query)
            logger.info(f"RAG 결과: {rag_result}")
            parsed_recommendations = self._parse_rag_recommendations(rag_result)
            if not parsed_recommendations:
                parsed_recommendations = [{"name": f"{food_name} 유사 음식 {i+1}", "reason": "dummy reason"} for i in range(limit)]
                logger.info(f"더미 parsed_recommendations 생성: {parsed_recommendations}")
            return {
                "reference_food": food_name,
                "similar_foods": parsed_recommendations,
                "source": "rag"
            }


    def get_recipe_recommendations(
            self,
            ingredients: List[str] = [],
            meal_type: str = "",
            health_goal: str = "",
            allergies: List[str] = [],
            query: str = None,  # 검색어 추가
            limit: int = 3
    ) -> List[Dict[str, Any]]:
        """
        레시피 추천 및 검색 통합 메서드

        Args:
            ingredients (List[str]): 사용 가능한 재료 목록
            meal_type (str): 식사 유형 (아침, 점심, 저녁)
            health_goal (str): 건강 목표
            allergies (List[str]): 알레르기 정보
            query (str, optional): 검색어
            limit (int, optional): 반환할 최대 레시피 수

        Returns:
            List[Dict[str, Any]]: 추천 레시피 목록
        """
        try:
            logger.info("레시피 추천/검색 시작")

            # 검색어가 있는 경우 ingredients에 추가
            if query:
                ingredients.append(query)

            # 쿼리 구성
            recipe_query = "레시피 추천"

            if meal_type:
                recipe_query += f", 식사: {meal_type}"

            if health_goal:
                recipe_query += f", 목표: {health_goal}"

            if ingredients:
                recipe_query += f", 재료: {', '.join(ingredients[:5])}"
                if len(ingredients) > 5:
                    recipe_query += f" 외 {len(ingredients) - 5}개"

            if allergies:
                recipe_query += f", 알레르기 제외: {', '.join(allergies)}"

            # RAG를 통한 레시피 추천
            rag_result = self.rag_service.query_food_info(recipe_query)

            # 결과 파싱 및 구조화
            recommended_recipes = self._parse_recipes(rag_result)

            logger.info(f"레시피 추천/검색 완료: {len(recommended_recipes)}개 레시피 추천됨")
            return recommended_recipes[:limit]

        except Exception as e:
            logger.error(f"레시피 추천/검색 중 오류 발생: {str(e)}")
            return []

    def generate_meal_recommendations(self, user: Optional[User], allergies: List[str] = [], recent_foods: List[str] = []) -> Dict[str, List[Dict[str, Any]]]:
        """
        사용자 맞춤형 식단 추천 생성

        Args:
            user (Optional[User]): 사용자 정보
            allergies (List[str]): 알레르기 정보
            recent_foods (List[str]): 최근 먹은 음식 목록

        Returns:
            Dict[str, List[Dict[str, Any]]]: 카테고리별 추천 목록
        """
        try:
            logger.info("식단 추천 생성 시작")

            recommendations = {
                "health_based": [],  # 건강 목표 기반 추천
                "balanced_meal": [],  # 균형 잡힌 식단 추천
                "variety_based": []   # 다양성 기반 추천 (최근에 먹지 않은 음식)
            }

            # 건강 목표 기반 쿼리 생성
            health_goal_query = ""
            if user and user.health_goal:
                health_goal = user.health_goal.lower()
                health_goal_query = f"건강 목표: {health_goal}"

                if "체중 감량" in health_goal or "다이어트" in health_goal:
                    health_goal_query += ", 저칼로리 고단백 식품"
                elif "근육 증가" in health_goal or "벌크업" in health_goal:
                    health_goal_query += ", 고단백 고칼로리 식품"
                elif "당뇨" in health_goal:
                    health_goal_query += ", 저탄수화물 식품"
                elif "고혈압" in health_goal:
                    health_goal_query += ", 저나트륨 식품"

            # 알레르기 정보 추가
            if allergies:
                health_goal_query += f", 알레르기 제외: {', '.join(allergies)}"

            # RAG 활용 건강 기반 추천
            if health_goal_query:
                try:
                    rag_result = self.rag_service.query_food_info(
                        f"다음 조건에 맞는 식품 추천: {health_goal_query}"
                    )
                    health_recommendations = self._parse_rag_recommendations(rag_result)

                    # 데이터베이스에서 추가 정보 보강
                    for rec in health_recommendations:
                        food_name = rec.get("name", "")
                        food_info = self.food_db.get_food_by_name(food_name)
                        if food_info:
                            rec["details"] = food_info
                            rec["source"] = "database"
                        else:
                            rec["source"] = "rag"

                    recommendations["health_based"] = health_recommendations[:3]
                except Exception as e:
                    logger.error(f"건강 기반 추천 중 오류: {str(e)}")

            # 균형 잡힌 식단 추천
            try:
                balanced_query = "균형 잡힌 한식 식단 조합 3가지 추천"
                if allergies:
                    balanced_query += f", 제외 재료: {', '.join(allergies)}"

                rag_result = self.rag_service.query_food_info(balanced_query)
                balanced_recommendations = self._parse_balanced_meal(rag_result)

                # 데이터베이스에서 각 구성요소 정보 보강
                for meal in balanced_recommendations:
                    components = []
                    for component in meal.get("components", []):
                        food_name = component.get("name", "")
                        food_info = self.food_db.get_food_by_name(food_name)
                        if food_info:
                            component["details"] = food_info
                            component["source"] = "database"
                        else:
                            component["source"] = "rag"
                        components.append(component)
                    meal["components"] = components

                recommendations["balanced_meal"] = balanced_recommendations[:3]
            except Exception as e:
                logger.error(f"균형 잡힌 식단 추천 중 오류: {str(e)}")

            # 다양성 기반 추천 (최근에 먹지 않은 음식)
            try:
                # 데이터베이스에서 모든 음식 가져오기
                all_foods = self.food_db.get_all_foods(limit=50)  # 적절한 수로 제한

                # 최근 먹은 음식 제외
                recent_food_set = set(recent_foods)
                not_recent_foods = [f for f in all_foods if f.get("name") not in recent_food_set]

                # 추천 생성
                import random
                selected_foods = random.sample(
                    not_recent_foods,
                    min(3, len(not_recent_foods))
                ) if not_recent_foods else []

                variety_based = []
                for food in selected_foods:
                    variety_based.append({
                        "name": food.get("name", ""),
                        "category": food.get("category", ""),
                        "reason": "최근에 드시지 않은 음식으로, 식단의 다양성을 높여줍니다.",
                        "details": food,
                        "source": "database"
                    })

                # 충분한 추천이 없으면 RAG 시스템 사용
                if len(variety_based) < 3:
                    variety_query = "다양한 한식 추천"
                    if recent_foods:
                        variety_query += f", 최근 먹은 음식 제외: {', '.join(recent_foods[:5])}"

                    rag_result = self.rag_service.query_food_info(variety_query)
                    rag_recommendations = self._parse_rag_recommendations(rag_result)

                    # 이미 추천된 음식 제외
                    existing_names = {item.get("name", "") for item in variety_based}
                    filtered_recs = [r for r in rag_recommendations if r.get("name", "") not in existing_names]

                    # 데이터베이스에서 추가 정보 보강
                    for rec in filtered_recs:
                        food_name = rec.get("name", "")
                        food_info = self.food_db.get_food_by_name(food_name)
                        if food_info:
                            rec["details"] = food_info
                            rec["source"] = "database"
                        else:
                            rec["source"] = "rag"

                    variety_based.extend(filtered_recs[:3 - len(variety_based)])

                recommendations["variety_based"] = variety_based
            except Exception as e:
                logger.error(f"다양성 기반 추천 중 오류: {str(e)}")

            logger.info(f"식단 추천 생성 완료: {sum(len(recs) for recs in recommendations.values())}개 추천")
            return recommendations

        except Exception as e:
            logger.error(f"식단 추천 생성 중 오류 발생: {str(e)}")
            return {
                "health_based": [],
                "balanced_meal": [],
                "variety_based": []
            }

    def generate_food_alternatives(self, food_name: str, health_goal: str = "", allergies: List[str] = [], limit: int = 3) -> List[Dict[str, Any]]:
        """
        식품 대체제 추천

        Args:
            food_name (str): 기준 식품 이름
            health_goal (str): 건강 목표
            allergies (List[str]): 알레르기 정보
            limit (int): 추천 개수

        Returns:
            List[Dict[str, Any]]: 추천 식품 목록
        """
        try:
            logger.info(f"식품 대체제 추천 시작: {food_name}")

            # 쿼리 구성
            query = f"{food_name}의 건강한 대체 식품"

            if health_goal:
                query += f", 건강 목표: {health_goal}"

            if allergies:
                query += f", 알레르기 제외: {', '.join(allergies)}"

            # RAG 활용 대체 식품 추천
            rag_result = self.rag_service.query_food_info(query)
            alternatives = self._parse_rag_recommendations(rag_result)

            # 데이터베이스에서 추가 정보 보강
            for alt in alternatives:
                alt_name = alt.get("name", "")
                food_info = self.food_db.get_food_by_name(alt_name)
                if food_info:
                    alt["details"] = food_info
                    alt["source"] = "database"
                else:
                    alt["source"] = "rag"

            logger.info(f"식품 대체제 추천 완료: {len(alternatives)}개 추천됨")
            return alternatives[:limit]

        except Exception as e:
            logger.error(f"식품 대체제 추천 중 오류 발생: {str(e)}")
            return []

    def _parse_rag_recommendations(self, rag_result):
        """RAG 결과에서 추천 식품 목록 추출"""
        try:
            lines = rag_result.split("\n")
            recommendations = []

            for line in lines:
                if ":" in line:
                    parts = line.split(":", 1)
                    if len(parts) == 2:
                        name = parts[1].strip()
                        reason = parts[0].strip()
                        if name:
                            recommendations.append({"name": name, "reason": reason})
                elif "." in line:
                    parts = line.split(".", 1)
                    if len(parts) > 1 and parts[0].strip().isdigit():
                        name = parts[1].strip()
                        if name:
                            recommendations.append({"name": name})
                elif "-" in line:
                    parts = line.split("-", 1)
                    if len(parts) > 1:
                        name = parts[1].strip()
                        if name:
                            recommendations.append({"name": name})

            return recommendations
        except Exception as e:
            logger.error(f"추천 결과 파싱 중 오류: {str(e)}")
            return []

    def _parse_balanced_meal(self, rag_result):
        """RAG 결과에서 균형 잡힌 식단 추출"""
        try:
            lines = rag_result.split("\n")
            meals = []
            current_meal = None

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # 새로운 식단 조합 시작
                if line.startswith("식단") or line.startswith("1.") or line.startswith("2.") or line.startswith("3."):
                    if current_meal:
                        meals.append(current_meal)

                    current_meal = {
                        "name": line.split(":", 1)[-1].strip() if ":" in line else line,
                        "components": []
                    }

                # 구성 음식 추가
                elif current_meal and (":" in line or "-" in line or "•" in line):
                    delimiter = ":" if ":" in line else "-" if "-" in line else "•"
                    parts = line.split(delimiter, 1)

                    if len(parts) > 1:
                        category = parts[0].strip()
                        name = parts[1].strip()

                        if name:
                            current_meal["components"].append({
                                "name": name,
                                "category": category
                            })

            # 마지막 식단 추가
            if current_meal and current_meal not in meals:
                meals.append(current_meal)

            # 각 식단에 이유 추가
            for meal in meals:
                meal["reason"] = "영양 균형이 잘 맞는 한식 식단입니다."

            return meals
        except Exception as e:
            logger.error(f"식단 조합 파싱 중 오류: {str(e)}")
            return []

    def _parse_recipes(self, recipes_json):
        """RAG 결과에서 레시피 정보 추출"""
        try:
            recipes = []
            for recipe in recipes_json["recipes"]:
                name = recipe.get("음식명", "이름 없음")
                ingredients = recipe.get("재료", [])
                instructions = recipe.get("조리법", "조리법 정보 없음")  # RAG 모델이 제공하는 조리법 사용

                # 데이터 구조 확인 후 저장
                recipes.append({
                    "title": name,
                    "ingredients": ingredients,
                    "instructions": instructions
                })

            return recipes
        except Exception as e:
            logger.error(f"레시피 파싱 중 오류: {str(e)}")
            return []




def search_recipes(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    독립적인 레시피 검색 함수

    Args:
        query (str): 검색어
        limit (int, optional): 반환할 최대 레시피 수. 기본값은 5.

    Returns:
        List[Dict[str, Any]]: 검색된 레시피 목록
    """
    # 환경 변수에서 OpenAI API 키 가져오기
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")

    # RAG 서비스를 명시적으로 API 키와 함께 생성
    rag_service = RAGService(openai_api_key=openai_api_key)
    service = RecommendationService(rag_service=rag_service)
    return service.get_recipe_recommendations(query=query, limit=limit)


# 클래스 외부에 래퍼 함수 정의
def generate_meal_recommendations(user=None, allergies=None, recent_foods=None):
    """RecommendationService.generate_meal_recommendations의 래퍼 함수"""
    # 환경 변수에서 OpenAI API 키 가져오기
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")

    # RAG 서비스를 명시적으로 API 키와 함께 생성
    rag_service = RAGService(openai_api_key=openai_api_key)
    service = RecommendationService(rag_service=rag_service)
    return service.generate_meal_recommendations(user, allergies or [], recent_foods or [])

def generate_food_alternatives(food_name, health_goal="", allergies=None, limit=3):
    """RecommendationService.generate_food_alternatives의 래퍼 함수"""
    # 환경 변수에서 OpenAI API 키 가져오기
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")

    # RAG 서비스를 명시적으로 API 키와 함께 생성
    rag_service = RAGService(openai_api_key=openai_api_key)
    service = RecommendationService(rag_service=rag_service)
    return service.generate_food_alternatives(food_name, health_goal, allergies or [], limit)
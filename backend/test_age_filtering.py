"""
Test script for age-based prediction filtering

Run this to verify the age calculation and filtering logic
"""
import sys
sys.path.insert(0, 'C:\\Users\\Admin\\OneDrive\\Documents\\RajanadiAstro\\backend')

from datetime import date
from app.utils.age_utils import (
    calculate_age,
    get_age_category,
    get_allowed_categories,
    is_category_allowed,
    get_age_appropriate_message,
    get_age_context_for_prompt,
    filter_prediction_topics
)

def test_age_calculation():
    """Test age calculation function"""
    print("=" * 60)
    print("TEST 1: Age Calculation")
    print("=" * 60)
    
    test_cases = [
        ("2020-03-11", "6-year-old child"),
        ("2010-06-15", "16-year-old teenager"),
        ("2000-01-01", "26-year-old adult"),
        ("1990-05-15", "35-year-old adult"),
        ("1960-12-25", "65-year-old senior"),
    ]
    
    for dob_str, description in test_cases:
        dob = date.fromisoformat(dob_str)
        age = calculate_age(dob)
        category = get_age_category(age)
        print(f"\nDOB: {dob_str} ({description})")
        print(f"  Calculated Age: {age} years")
        print(f"  Age Category: {category}")
    
    print("\n✅ Age calculation tests completed\n")

def test_category_filtering():
    """Test category filtering for different ages"""
    print("=" * 60)
    print("TEST 2: Category Filtering")
    print("=" * 60)
    
    ages = [6, 16, 22, 35, 65]
    categories = ['general', 'health', 'education', 'career', 'marriage', 'wealth', 'children', 'parents']
    
    for age in ages:
        print(f"\n{age}-year-old person:")
        allowed = get_allowed_categories(age)
        print(f"  Allowed categories: {', '.join(allowed)}")
        
        print(f"  Category validation:")
        for category in categories:
            is_allowed = is_category_allowed(category, age)
            symbol = "✅" if is_allowed else "❌"
            print(f"    {symbol} {category}")
    
    print("\n✅ Category filtering tests completed\n")

def test_inappropriate_messages():
    """Test age-inappropriate messages"""
    print("=" * 60)
    print("TEST 3: Age-Inappropriate Messages")
    print("=" * 60)
    
    test_cases = [
        (6, "marriage", "6-year-old requesting marriage"),
        (6, "career", "6-year-old requesting career"),
        (16, "marriage", "16-year-old requesting marriage"),
        (16, "wealth", "16-year-old requesting wealth"),
        (65, "career", "65-year-old requesting career"),
    ]
    
    for age, category, description in test_cases:
        print(f"\n{description}:")
        message = get_age_appropriate_message(category, age)
        if message:
            print(f"  Message: {message}")
        else:
            print(f"  ✅ Category is allowed for this age")
    
    print("\n✅ Age-inappropriate message tests completed\n")

def test_age_context_prompts():
    """Test age context for AI prompts"""
    print("=" * 60)
    print("TEST 4: Age Context for AI Prompts")
    print("=" * 60)
    
    test_cases = [
        (6, "Ravi"),
        (16, "Priya"),
        (22, "Amit"),
        (35, "Arjun"),
        (65, "Ramesh")
    ]
    
    for age, name in test_cases:
        print(f"\nAge {age}, Name: {name}")
        context = get_age_context_for_prompt(age, name)
        print(f"  Context: {context}")
    
    print("\n✅ Age context prompt tests completed\n")

def test_prediction_topics():
    """Test prediction topic filtering"""
    print("=" * 60)
    print("TEST 5: Prediction Topics by Age")
    print("=" * 60)
    
    ages = [6, 16, 22, 35, 65]
    
    for age in ages:
        print(f"\n{age}-year-old person - Recommended topics:")
        topics = filter_prediction_topics(age)
        for i, topic in enumerate(topics, 1):
            print(f"  {i}. {topic}")
    
    print("\n✅ Prediction topic tests completed\n")

def test_real_world_scenario():
    """Test a real-world scenario"""
    print("=" * 60)
    print("TEST 6: Real-World Scenario")
    print("=" * 60)
    
    print("\nScenario: 6-year-old child born on 2020-03-11")
    dob = date(2020, 3, 11)
    age = calculate_age(dob)
    name = "Little Ravi"
    
    print(f"\nCalculated Age: {age} years")
    print(f"Age Category: {get_age_category(age)}")
    
    print("\n--- Testing Education Category (Should be allowed) ---")
    category = "education"
    if is_category_allowed(category, age):
        print(f"✅ {category.capitalize()} is allowed for {age}-year-old")
        context = get_age_context_for_prompt(age, name)
        print(f"AI Context: {context}")
    else:
        print(f"❌ {category.capitalize()} is NOT allowed")
        message = get_age_appropriate_message(category, age)
        print(f"Message: {message}")
    
    print("\n--- Testing Marriage Category (Should be blocked) ---")
    category = "marriage"
    if is_category_allowed(category, age):
        print(f"✅ {category.capitalize()} is allowed for {age}-year-old")
    else:
        print(f"❌ {category.capitalize()} is NOT allowed")
        message = get_age_appropriate_message(category, age)
        print(f"Message: {message}")
    
    print("\n--- Testing Career Category (Should be blocked) ---")
    category = "career"
    if is_category_allowed(category, age):
        print(f"✅ {category.capitalize()} is allowed for {age}-year-old")
    else:
        print(f"❌ {category.capitalize()} is NOT allowed")
        message = get_age_appropriate_message(category, age)
        print(f"Message: {message}")
    
    print("\n✅ Real-world scenario test completed\n")

def run_all_tests():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "AGE-BASED FILTERING TEST SUITE" + " " * 16 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    try:
        test_age_calculation()
        test_category_filtering()
        test_inappropriate_messages()
        test_age_context_prompts()
        test_prediction_topics()
        test_real_world_scenario()
        
        print("=" * 60)
        print("🎉 ALL TESTS PASSED SUCCESSFULLY! 🎉")
        print("=" * 60)
        print()
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_all_tests()

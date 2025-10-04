#!/usr/bin/env python3
"""
Test script for AI-Powered Travel Intelligence Features
"""

def test_imports():
    """Test that all new modules can be imported"""
    try:
        from intelligence_agents import IntelligenceAgents
        from intelligence_tasks import IntelligenceTasks
        from tools.risk_assessment_tools import RiskAssessmentTools
        from tools.crowd_density_tools import CrowdDensityTools
        from tools.price_optimization_tools import PriceOptimizationTools
        from tools.language_barrier_tools import LanguageBarrierTools
        print("✅ All intelligence modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_agents_creation():
    """Test that intelligence agents can be created"""
    try:
        from intelligence_agents import IntelligenceAgents
        from crewai import LLM
        
        llm = LLM(model="gemini/gemini-2.0-flash")
        agents = IntelligenceAgents(llm=llm)
        
        # Test agent creation
        risk_agent = agents.risk_assessment_agent()
        crowd_agent = agents.crowd_density_agent()
        price_agent = agents.price_optimization_agent()
        lang_agent = agents.language_barrier_agent()
        
        print("✅ All intelligence agents created successfully")
        return True
    except Exception as e:
        print(f"❌ Agent creation error: {e}")
        return False

def test_tools_creation():
    """Test that intelligence tools can be created"""
    try:
        from tools.risk_assessment_tools import RiskAssessmentTools
        from tools.crowd_density_tools import CrowdDensityTools
        from tools.price_optimization_tools import PriceOptimizationTools
        from tools.language_barrier_tools import LanguageBarrierTools
        
        # Test tool creation
        risk_tool = RiskAssessmentTools()
        crowd_tool = CrowdDensityTools()
        price_tool = PriceOptimizationTools()
        lang_tool = LanguageBarrierTools()
        
        print("✅ All intelligence tools created successfully")
        return True
    except Exception as e:
        print(f"❌ Tool creation error: {e}")
        return False

def test_cli_integration():
    """Test CLI integration"""
    try:
        from cli_app import TripCrew
        from datetime import date
        
        # Test basic TripCrew creation
        trip_crew = TripCrew(
            origin="New York",
            cities="Tokyo",
            date_range="2025-06-01 to 2025-06-10",
            interests="2 adults who love culture",
            enable_intelligence=True
        )
        
        print("✅ CLI integration test passed")
        return True
    except Exception as e:
        print(f"❌ CLI integration error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧠 Testing AI-Powered Travel Intelligence Features")
    print("=" * 60)
    
    tests = [
        ("Import Test", test_imports),
        ("Agent Creation Test", test_agents_creation),
        ("Tool Creation Test", test_tools_creation),
        ("CLI Integration Test", test_cli_integration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Intelligence features are ready to use.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    main()

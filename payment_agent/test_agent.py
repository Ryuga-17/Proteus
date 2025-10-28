#!/usr/bin/env python3
"""
Comprehensive test script for the Payment Agent system.
This script tests individual components and full agent workflows.
"""

import json
import sys
from datetime import datetime

# Test imports
try:
    from tools import PaymentTools
    from agents import sales_agent, payment_agent, loyalty_agent
    from tasks import task_fail_scenario, task_kiosk_scenario, task_points_scenario
    from crewai import Crew, Process
    print("✅ All imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

def test_individual_tools():
    """Test each payment tool individually"""
    print("\n" + "="*50)
    print("TESTING INDIVIDUAL TOOLS")
    print("="*50)
    
    # Test 1: Standard payment success
    print("\n1. Testing standard payment (success case):")
    result = PaymentTools.process_standard_payment(
        customer_id="test-customer-123",
        amount=50.00,
        payment_method="credit_card",
        details={"card_number": "1234-5678-9012-3456"}
    )
    print(f"   Result: {result}")
    
    # Test 2: Standard payment failure
    print("\n2. Testing standard payment (failure case):")
    result = PaymentTools.process_standard_payment(
        customer_id="test-customer-456",
        amount=100.00,
        payment_method="credit_card",
        details={"card_number": "fail-1234"}
    )
    print(f"   Result: {result}")
    
    # Test 3: Kiosk handoff
    print("\n3. Testing kiosk-to-mobile handoff:")
    result = PaymentTools.generate_kiosk_to_mobile_handoff(
        customer_id="test-customer-789",
        amount=75.50,
        session_id="kiosk-test-001"
    )
    print(f"   Result: {result}")
    
    # Test 4: Loyalty points success
    print("\n4. Testing loyalty points (success case):")
    result = PaymentTools.debit_loyalty_points(
        customer_id="test-customer-999",
        points_to_debit=500
    )
    print(f"   Result: {result}")
    
    # Test 5: Loyalty points failure
    print("\n5. Testing loyalty points (failure case):")
    result = PaymentTools.debit_loyalty_points(
        customer_id="test-customer-888",
        points_to_debit=1500
    )
    print(f"   Result: {result}")

def test_agent_initialization():
    """Test that all agents can be initialized properly"""
    print("\n" + "="*50)
    print("TESTING AGENT INITIALIZATION")
    print("="*50)
    
    agents = [sales_agent, payment_agent, loyalty_agent]
    agent_names = ["Sales Agent", "Payment Agent", "Loyalty Agent"]
    
    for agent, name in zip(agents, agent_names):
        try:
            print(f"\n✅ {name}:")
            print(f"   Role: {agent.role}")
            print(f"   Goal: {agent.goal[:50]}...")
            print(f"   Tools: {len(agent.tools) if hasattr(agent, 'tools') and agent.tools else 0}")
            print(f"   Delegation: {agent.allow_delegation}")
        except Exception as e:
            print(f"❌ {name} initialization failed: {e}")

def test_task_definitions():
    """Test that all tasks are properly defined"""
    print("\n" + "="*50)
    print("TESTING TASK DEFINITIONS")
    print("="*50)
    
    tasks = [task_fail_scenario, task_kiosk_scenario, task_points_scenario]
    task_names = ["Fail Scenario", "Kiosk Scenario", "Points Scenario"]
    
    for task, name in zip(tasks, task_names):
        try:
            print(f"\n✅ {name}:")
            print(f"   Description: {task.description[:100]}...")
            print(f"   Expected Output: {task.expected_output[:50]}...")
            print(f"   Agent: {task.agent.role if task.agent else 'None'}")
        except Exception as e:
            print(f"❌ {name} task definition failed: {e}")

def test_crew_assembly():
    """Test that the crew can be assembled properly"""
    print("\n" + "="*50)
    print("TESTING CREW ASSEMBLY")
    print("="*50)
    
    try:
        # Test with just the fail scenario first
        crew = Crew(
            agents=[sales_agent, payment_agent, loyalty_agent],
            tasks=[task_fail_scenario],
            process=Process.hierarchical,
            manager_llm=None,
            verbose=1
        )
        print("✅ Crew assembly successful")
        print(f"   Agents: {len(crew.agents)}")
        print(f"   Tasks: {len(crew.tasks)}")
        print(f"   Process: {crew.process}")
        return crew
    except Exception as e:
        print(f"❌ Crew assembly failed: {e}")
        return None

def run_single_scenario_test(crew, scenario_name, task):
    """Run a single scenario test"""
    print(f"\n--- Testing {scenario_name} ---")
    
    try:
        # Create a minimal crew for this test
        test_crew = Crew(
            agents=[sales_agent, payment_agent, loyalty_agent],
            tasks=[task],
            process=Process.hierarchical,
            manager_llm=None,
            verbose=1
        )
        
        print(f"Running {scenario_name}...")
        result = test_crew.kickoff()
        
        print(f"✅ {scenario_name} completed")
        print(f"Result: {result}")
        return True
        
    except Exception as e:
        print(f"❌ {scenario_name} failed: {e}")
        return False

def main():
    """Main test runner"""
    print("🚀 PAYMENT AGENT TESTING SUITE")
    print("="*50)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test individual components
    test_individual_tools()
    test_agent_initialization()
    test_task_definitions()
    
    # Test crew assembly
    crew = test_crew_assembly()
    
    if crew:
        print("\n" + "="*50)
        print("TESTING FULL SCENARIOS")
        print("="*50)
        
        # Test individual scenarios
        scenarios = [
            ("Fail Scenario", task_fail_scenario),
            ("Kiosk Scenario", task_kiosk_scenario),
            ("Points Scenario", task_points_scenario)
        ]
        
        results = []
        for name, task in scenarios:
            success = run_single_scenario_test(crew, name, task)
            results.append((name, success))
        
        # Summary
        print("\n" + "="*50)
        print("TEST SUMMARY")
        print("="*50)
        
        passed = sum(1 for _, success in results if success)
        total = len(results)
        
        for name, success in results:
            status = "✅ PASSED" if success else "❌ FAILED"
            print(f"{status} {name}")
        
        print(f"\nOverall: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! Your payment agent is working properly.")
        else:
            print("⚠️  Some tests failed. Check the output above for details.")
    else:
        print("❌ Cannot run scenario tests due to crew assembly failure")

if __name__ == "__main__":
    main()

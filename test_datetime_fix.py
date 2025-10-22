"""
Test script to verify datetime functionality is working correctly
"""

def test_datetime_imports():
    """Test that datetime imports work correctly"""
    try:
        from datetime import datetime as dt, timedelta
        
        print("✅ DateTime imports successful")
        
        # Test basic datetime operations
        current_date = dt.now()
        print(f"✅ Current date: {current_date}")
        
        # Test date arithmetic
        three_months_out = current_date + timedelta(days=90)
        print(f"✅ Three months out: {three_months_out}")
        
        # Test date parsing
        test_date_str = "2025-12-15"
        parsed_date = dt.strptime(test_date_str, '%Y-%m-%d')
        print(f"✅ Parsed date: {parsed_date}")
        
        # Test comparison
        is_within_range = parsed_date <= three_months_out
        print(f"✅ Date comparison: {is_within_range}")
        
        print("\n🎉 All datetime operations working correctly!")
        
    except Exception as e:
        print(f"❌ DateTime error: {e}")
        import traceback
        traceback.print_exc()

def test_column_filtering():
    """Test the column filtering logic"""
    try:
        from datetime import datetime as dt, timedelta
        import pandas as pd
        
        # Create sample columns like what we'd get from options data
        sample_columns = [
            '2025-10-25', '2025-11-01', '2025-11-15', '2025-12-01', 
            '2025-12-15', '2026-01-01', '2026-02-01', '2026-03-01'
        ]
        
        print(f"Sample columns: {sample_columns}")
        
        # Test 3-month filtering
        current_date = dt.now()
        three_months_out = current_date + timedelta(days=90)
        
        relevant_columns = []
        for col in sample_columns:
            try:
                col_date = dt.strptime(str(col), '%Y-%m-%d')
                if col_date <= three_months_out:
                    relevant_columns.append(col)
            except (ValueError, TypeError):
                relevant_columns.append(col)
        
        print(f"✅ Filtered columns (3 months): {relevant_columns}")
        print(f"✅ Filtered {len(sample_columns)} -> {len(relevant_columns)} columns")
        
    except Exception as e:
        print(f"❌ Column filtering error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Testing datetime functionality...")
    print("=" * 50)
    
    test_datetime_imports()
    print("\n" + "=" * 50)
    
    test_column_filtering()
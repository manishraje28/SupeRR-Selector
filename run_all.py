import time
import subprocess
import sys
import os

def run_step(script_name, description):
    print(f"\n==================================================")
    print(f"▶ RUNNING: {description} ({script_name})")
    print(f"==================================================")
    start_time = time.time()
    result = subprocess.run([sys.executable, script_name], capture_output=True, text=True)
    duration = time.time() - start_time
    
    if result.returncode != 0:
        print(f"❌ ERROR in {script_name} (exited with code {result.returncode}):")
        print(result.stderr)
        sys.exit(1)
    else:
        print(result.stdout)
        print(f"✅ COMPLETED {script_name} in {duration:.2f} seconds.")

def main():
    total_start = time.time()
    print("=" * 60)
    print("🚀 SUPERR SELECTOR SEASON 2: END-TO-END PIPELINE EXECUTION")
    print("=" * 60)

    steps = [
        ("src/01_data_pipeline.py", "Step 1: Data Ingestion & State Reconstruction"),
        ("src/02_pressure_engine.py", "Step 2: Match Pressure & Leverage Modeling"),
        ("src/03_performance_cava.py", "Step 3: CAVA Expectation Models & Context Adjustment"),
        ("src/04_ratings_and_rankings.py", "Step 4: Empirical Bayes Ratings & Sensitivity"),
        ("src/build_comprehensive_database.py", "Step 5: Comprehensive War Room Database & Census Generation"),
        ("src/05_generate_report_pdf.py", "Step 6: Official Methodology Report PDF Generation"),
        ("scripts/generate_standalone_dashboard.py", "Step 7: Standalone Offline Dashboard HTML Compilation")
    ]

    for script, desc in steps:
        run_step(script, desc)

    total_duration = time.time() - total_start
    print("\n" + "=" * 60)
    print(f"🎉 FULL PIPELINE COMPLETED SUCCESSFULLY IN {total_duration:.2f}s!")
    print("=" * 60)
    print("\nGenerated Artifacts in outputs/:")
    for fname in sorted(os.listdir('outputs')):
        fpath = os.path.join('outputs', fname)
        size_kb = os.path.getsize(fpath) / 1024
        print(f" - outputs/{fname} ({size_kb:.1f} KB)")

if __name__ == '__main__':
    main()

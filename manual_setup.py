
"""Manual framework setup without import issues"""

import shutil
from pathlib import Path

print("🔧 Manual Framework Setup")
print("=========================")

# Source and destination paths
src = Path("/Users/kimr/tulok/sample-java-framework")
dst = Path("data/framework")

# Check source exists
if not src.exists():
    print(f"❌ Source not found: {src}")
    print("Available options:")
    for possible in ["sample-java-framework", "/Users/kimr/tulok/sample-java-framework"]:
        if Path(possible).exists():
            print(f"   ✅ {possible}")
    exit(1)

print(f"📁 Source: {src}")
print(f"📁 Target: {dst}")

# Create target directory
dst.parent.mkdir(exist_ok=True)

# Remove existing target if it exists
if dst.exists():
    shutil.rmtree(dst)

# Copy framework
shutil.copytree(src, dst)
print("✅ Framework copied successfully")

# Verify Java files
java_files = list(dst.glob("**/*.java"))
print(f"📄 Found {len(java_files)} Java files")

# Count step definitions
step_count = 0
for java_file in java_files:
    try:
        with open(java_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            step_count += content.count("@Given")
            step_count += content.count("@When") 
            step_count += content.count("@Then")
    except Exception as e:
        print(f"⚠️ Could not read {java_file}: {e}")

print(f"📋 Found {step_count} step definitions")

# Show sample step definitions
print("\n📋 Sample step definitions:")
sample_count = 0
for java_file in java_files:
    if sample_count >= 3:
        break
    try:
        with open(java_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')
            for line in lines:
                if '@Given' in line or '@When' in line or '@Then' in line:
                    print(f"   {line.strip()}")
                    sample_count += 1
                    if sample_count >= 3:
                        break
    except:
        pass

# Create .env file
env_content = f"FRAMEWORK_PATH={dst.absolute()}\n"
with open(".env", "w") as f:
    f.write(env_content)

print(f"\n✅ Setup complete!")
print(f"📊 Summary:")
print(f"   - Java files: {len(java_files)}")
print(f"   - Step definitions: {step_count}")
print(f"   - Framework path: {dst.absolute()}")
print(f"\n🚀 Next steps:")
print(f"   python scripts/train.py")
print(f"   OR python simple_train.py")
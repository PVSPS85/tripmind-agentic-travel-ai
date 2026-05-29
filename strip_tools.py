import glob
import re

for filepath in glob.glob('/Users/pranav/tripai /tripmind-agentic-travel-ai/ai-agents/agents/*.py'):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Remove tools=[SearchTools.search_internet]
    new_content = re.sub(r'tools=\[SearchTools\.search_internet\],?\s*(?:#.*)?', 'tools=[],', content)
    
    # Handle the case where WeatherTools is also there
    new_content = re.sub(r'tools=\[SearchTools\.search_internet,\s*WeatherTools\.get_weather\],?', 'tools=[WeatherTools.get_weather],', new_content)
    
    with open(filepath, 'w') as f:
        f.write(new_content)
    print(f"Cleaned {filepath}")

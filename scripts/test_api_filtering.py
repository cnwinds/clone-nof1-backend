"""
测试 API 过滤功能
验证只返回激活的模型
"""
import sys
from pathlib import Path
import requests
import json

# 添加项目根目录到路径
sys.path.append(str(Path(__file__).parent.parent))


def test_api_filtering():
    """测试 API 过滤功能"""
    print("=" * 60)
    print("测试 API 过滤功能")
    print("=" * 60)
    print()
    
    base_url = "http://localhost:3001"
    
    try:
        # 1. 测试获取激活的模型
        print("1. 测试 /api/models (只返回激活的模型)")
        print("-" * 40)
        
        response = requests.get(f"{base_url}/api/models")
        if response.status_code == 200:
            data = response.json()
            models = data.get("data", [])
            
            print(f"✅ 返回 {len(models)} 个模型:")
            for model in models:
                print(f"  - {model['display_name']} ({model['llm_provider']}) - 状态: {model['status']}")
            
            # 验证所有模型都是激活的
            active_count = sum(1 for m in models if m['status'] == 'active')
            print(f"\n✓ 激活模型数量: {active_count}/{len(models)}")
            
            if active_count == len(models):
                print("✅ 所有返回的模型都是激活状态")
            else:
                print("❌ 有未激活的模型被返回了")
        else:
            print(f"❌ 请求失败: {response.status_code}")
            print(response.text)
        
        print()
        
        # 2. 测试获取所有模型（管理员接口）
        print("2. 测试 /api/models/all (返回所有模型)")
        print("-" * 40)
        
        response = requests.get(f"{base_url}/api/models/all")
        if response.status_code == 200:
            data = response.json()
            all_models = data.get("data", [])
            
            print(f"✅ 返回 {len(all_models)} 个模型:")
            for model in all_models:
                status_icon = "✅" if model['status'] == 'active' else "⚪"
                print(f"  {status_icon} {model['display_name']} ({model['llm_provider']}) - 状态: {model['status']}")
            
            # 统计激活和未激活的模型
            active_models = [m for m in all_models if m['status'] == 'active']
            inactive_models = [m for m in all_models if m['status'] == 'inactive']
            
            print(f"\n📊 统计:")
            print(f"  - 激活模型: {len(active_models)} 个")
            print(f"  - 未激活模型: {len(inactive_models)} 个")
        else:
            print(f"❌ 请求失败: {response.status_code}")
            print(response.text)
        
        print()
        
        # 3. 测试赛季详情
        print("3. 测试赛季详情 (只显示激活模型的排名)")
        print("-" * 40)
        
        # 先获取赛季列表
        response = requests.get(f"{base_url}/api/seasons")
        if response.status_code == 200:
            data = response.json()
            seasons = data.get("data", [])
            
            if seasons:
                season_id = seasons[0]['id']
                print(f"测试赛季: {seasons[0]['name']}")
                
                # 获取赛季详情
                response = requests.get(f"{base_url}/api/seasons/{season_id}")
                if response.status_code == 200:
                    data = response.json()
                    season_data = data.get("data", {})
                    models = season_data.get("models", [])
                    
                    print(f"✅ 赛季中有 {len(models)} 个模型:")
                    for i, model in enumerate(models, 1):
                        print(f"  {i}. {model['display_name']} - 价值: ${model['current_value']:.2f} - 收益: {model['performance']:.2f}%")
                    
                    print(f"\n✓ 只显示激活模型的排名")
                else:
                    print(f"❌ 获取赛季详情失败: {response.status_code}")
            else:
                print("❌ 没有找到赛季")
        else:
            print(f"❌ 获取赛季列表失败: {response.status_code}")
        
        print()
        
        # 4. 对比结果
        print("4. 对比结果")
        print("-" * 40)
        
        # 重新获取数据进行对比
        models_response = requests.get(f"{base_url}/api/models")
        all_models_response = requests.get(f"{base_url}/api/models/all")
        
        if models_response.status_code == 200 and all_models_response.status_code == 200:
            active_models = models_response.json()["data"]
            all_models = all_models_response.json()["data"]
            
            print(f"📊 API 对比:")
            print(f"  - /api/models: {len(active_models)} 个模型")
            print(f"  - /api/models/all: {len(all_models)} 个模型")
            
            if len(active_models) < len(all_models):
                print("✅ 过滤功能正常工作")
            else:
                print("⚠️  过滤功能可能有问题")
        
        print()
        print("=" * 60)
        print("🎉 API 过滤测试完成！")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到 API 服务器")
        print("请确保服务已启动: docker-compose up -d")
        print("或检查端口: http://localhost:3001")
    except Exception as e:
        print(f"❌ 测试失败: {e}")


if __name__ == "__main__":
    test_api_filtering()


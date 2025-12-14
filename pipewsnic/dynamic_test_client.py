import asyncio
import websockets
import sys

async def test_connect(path):
    uri = f"ws://localhost:8086{path}"
    print(f"Connecting to {uri}...")
    try:
        async with websockets.connect(uri) as websocket:
            print(f"SUCCESS: Connected to {path}")
            await websocket.close()
            return True
    except websockets.exceptions.InvalidStatusCode as e:
        print(f"FAILURE: {path} returned status {e.status_code}")
        return False
    except Exception as e:
        print(f"FAILURE: Could not connect to {path}: {e}")
        return False

async def main():
    print("Test 1: Connect to / (Should FAIL)")
    root_result = await test_connect("/")
    if root_result:
        print("ERROR: / should have been rejected!")
    else:
        print("PASS: / was rejected.")

    print("\nTest 2: Connect to /dyn1 (Should SUCCEED - Create New Group)")
    dyn1_result = await test_connect("/dyn1")
    if not dyn1_result:
        print("ERROR: /dyn1 failed!")
        sys.exit(1)

    print("\nTest 3: Connect to /dyn2 (Should SUCCEED - Create New Group)")
    dyn2_result = await test_connect("/dyn2")
    if not dyn2_result:
        print("ERROR: /dyn2 failed!")
        sys.exit(1)
        
    print("\nTest 4: Connect to /dyn1 again (Should SUCCEED - Reuse Group)")
    dyn1_reuse_result = await test_connect("/dyn1")
    if not dyn1_reuse_result:
        print("ERROR: /dyn1 reuse failed!")
        sys.exit(1)

    print("\nAll dynamic group tests passed.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass

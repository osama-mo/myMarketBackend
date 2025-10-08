#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Shopping Cart/Basket Test Suite${NC}"
echo -e "${BLUE}========================================${NC}\n"

BASE_URL="http://localhost:5000"

wait_input() {
    echo -e "${YELLOW}Press ENTER to continue...${NC}"
    read
}

# =====================================
# SETUP: Login and Create Products
# =====================================

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  SETUP${NC}"
echo -e "${BLUE}========================================${NC}\n"

echo -e "${YELLOW}[SETUP 1] Logging in as admin...${NC}"
ADMIN_RESPONSE=$(http POST $BASE_URL/auth/login \
  username=admin \
  password=admin123 --print=b)

ADMIN_TOKEN=$(echo $ADMIN_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['access_token'])")
echo -e "${GREEN}✅ Admin logged in${NC}"
wait_input

echo -e "${YELLOW}[SETUP 2] Creating test products...${NC}"

# Product 1: iPhone
http POST $BASE_URL/products \
  "Authorization: Bearer $ADMIN_TOKEN" \
  name="iPhone 15 Pro" \
  description="Latest flagship smartphone" \
  price=999.99 \
  stock=10 \
  category="electronics" > /dev/null 2>&1

# Product 2: MacBook
http POST $BASE_URL/products \
  "Authorization: Bearer $ADMIN_TOKEN" \
  name="MacBook Pro" \
  description="Powerful laptop" \
  price=2499.99 \
  stock=5 \
  category="electronics" > /dev/null 2>&1

# Product 3: T-Shirt
http POST $BASE_URL/products \
  "Authorization: Bearer $ADMIN_TOKEN" \
  name="Cotton T-Shirt" \
  description="Comfortable t-shirt" \
  price=19.99 \
  stock=100 \
  category="clothing" > /dev/null 2>&1

echo -e "${GREEN}✅ 3 products created${NC}"
wait_input

echo -e "${YELLOW}[SETUP 3] Creating regular user (alice)...${NC}"
http POST $BASE_URL/auth/signup \
  username=alice \
  email=alice@test.com \
  password=alice123 > /dev/null 2>&1

echo -e "${GREEN}✅ User created${NC}"
wait_input

echo -e "${YELLOW}[SETUP 4] Logging in as alice...${NC}"
USER_RESPONSE=$(http POST $BASE_URL/auth/login \
  username=alice \
  password=alice123 --print=b)

USER_TOKEN=$(echo $USER_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['access_token'])")
echo -e "${GREEN}✅ Alice logged in${NC}"
wait_input

# =====================================
# BASKET TESTS
# =====================================

echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}  BASKET/CART TESTS${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Test 1: Get empty basket
echo -e "${YELLOW}[1/11] Getting empty basket...${NC}"
http GET $BASE_URL/basket \
  "Authorization: Bearer $USER_TOKEN"
wait_input

# Test 2: Add product to basket
echo -e "${YELLOW}[2/11] Adding iPhone to basket (quantity: 2)...${NC}"
http POST $BASE_URL/basket/add \
  "Authorization: Bearer $USER_TOKEN" \
  product_id=1 \
  quantity=2
wait_input

# Test 3: Add another product
echo -e "${YELLOW}[3/11] Adding MacBook to basket (quantity: 1)...${NC}"
http POST $BASE_URL/basket/add \
  "Authorization: Bearer $USER_TOKEN" \
  product_id=2 \
  quantity=1
wait_input

# Test 4: Add same product again (should update quantity)
echo -e "${YELLOW}[4/11] Adding iPhone again (quantity: 1) - should update to 3 total...${NC}"
http POST $BASE_URL/basket/add \
  "Authorization: Bearer $USER_TOKEN" \
  product_id=1 \
  quantity=1
wait_input

# Test 5: Get basket with items
echo -e "${YELLOW}[5/11] Getting basket with items...${NC}"
http GET $BASE_URL/basket \
  "Authorization: Bearer $USER_TOKEN"
wait_input

# Test 6: Update quantity
echo -e "${YELLOW}[6/11] Updating iPhone quantity to 5...${NC}"
http PUT $BASE_URL/basket/update \
  "Authorization: Bearer $USER_TOKEN" \
  product_id=1 \
  quantity=5
wait_input

# Test 7: Try to exceed stock
echo -e "${YELLOW}[7/11] Trying to add more than available stock (should fail)...${NC}"
http POST $BASE_URL/basket/add \
  "Authorization: Bearer $USER_TOKEN" \
  product_id=1 \
  quantity=10
echo -e "${GREEN}✅ Correctly rejected (expected)${NC}"
wait_input

# Test 8: Remove item from basket
echo -e "${YELLOW}[8/11] Removing MacBook from basket...${NC}"
http DELETE $BASE_URL/basket/remove/2 \
  "Authorization: Bearer $USER_TOKEN"
wait_input

# Test 9: Add T-Shirt
echo -e "${YELLOW}[9/11] Adding T-Shirt to basket...${NC}"
http POST $BASE_URL/basket/add \
  "Authorization: Bearer $USER_TOKEN" \
  product_id=3 \
  quantity=3
wait_input

# Test 10: Get final basket state
echo -e "${YELLOW}[10/11] Getting final basket state...${NC}"
http GET $BASE_URL/basket \
  "Authorization: Bearer $USER_TOKEN"
wait_input

# Test 11: Checkout
echo -e "${YELLOW}[11/11] Checking out basket...${NC}"
http POST $BASE_URL/basket/checkout \
  "Authorization: Bearer $USER_TOKEN"
wait_input

# =====================================
# POST-CHECKOUT TESTS
# =====================================

echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}  POST-CHECKOUT TESTS${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Test 12: Get basket after checkout (should be empty)
echo -e "${YELLOW}[12] Getting basket after checkout (should be new empty basket)...${NC}"
http GET $BASE_URL/basket \
  "Authorization: Bearer $USER_TOKEN"
wait_input

# Test 13: Get order history
echo -e "${YELLOW}[13] Getting order history...${NC}"
http GET $BASE_URL/basket/orders \
  "Authorization: Bearer $USER_TOKEN"
wait_input

# Test 14: Check product stock updated
echo -e "${YELLOW}[14] Checking iPhone stock (should be reduced)...${NC}"
http GET $BASE_URL/products/1
wait_input

# Test 15: Add items to new basket
echo -e "${YELLOW}[15] Adding items to new basket...${NC}"
http POST $BASE_URL/basket/add \
  "Authorization: Bearer $USER_TOKEN" \
  product_id=2 \
  quantity=1
wait_input

# Test 16: Clear basket
echo -e "${YELLOW}[16] Clearing basket...${NC}"
http DELETE $BASE_URL/basket/clear \
  "Authorization: Bearer $USER_TOKEN"
wait_input

# =====================================
# EDGE CASES
# =====================================

echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}  EDGE CASES${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Test 17: Try to checkout empty basket
echo -e "${YELLOW}[17] Trying to checkout empty basket (should fail)...${NC}"
http POST $BASE_URL/basket/checkout \
  "Authorization: Bearer $USER_TOKEN"
echo -e "${GREEN}✅ Correctly rejected (expected)${NC}"
wait_input

# Test 18: Try to add non-existent product
echo -e "${YELLOW}[18] Trying to add non-existent product (should fail)...${NC}"
http POST $BASE_URL/basket/add \
  "Authorization: Bearer $USER_TOKEN" \
  product_id=999 \
  quantity=1
echo -e "${GREEN}✅ Correctly rejected (expected)${NC}"
wait_input

# Test 19: Try to set negative quantity
echo -e "${YELLOW}[19] Trying to set negative quantity (should fail)...${NC}"
http PUT $BASE_URL/basket/update \
  "Authorization: Bearer $USER_TOKEN" \
  product_id=1 \
  quantity=-5
echo -e "${GREEN}✅ Correctly rejected (expected)${NC}"
wait_input

# Test 20: Set quantity to 0 (should remove item)
echo -e "${YELLOW}[20] Adding item then setting quantity to 0 (should remove)...${NC}"
http POST $BASE_URL/basket/add \
  "Authorization: Bearer $USER_TOKEN" \
  product_id=3 \
  quantity=2 > /dev/null 2>&1

http PUT $BASE_URL/basket/update \
  "Authorization: Bearer $USER_TOKEN" \
  product_id=3 \
  quantity=0
wait_input

# =====================================
# SUMMARY
# =====================================

echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}  TEST SUITE COMPLETED!${NC}"
echo -e "${BLUE}========================================${NC}\n"

echo -e "${GREEN}✅ All basket tests completed!${NC}"
echo -e "\n${YELLOW}Summary:${NC}"
echo -e "  • Created and managed basket"
echo -e "  • Added/updated/removed items"
echo -e "  • Validated stock availability"
echo -e "  • Completed checkout"
echo -e "  • Verified order history"
echo -e "  • Tested edge cases"

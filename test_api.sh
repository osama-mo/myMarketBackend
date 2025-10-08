#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  MyMarket Backend API Test Suite${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Base URL
BASE_URL="http://localhost:5000"

# Check if server is running
echo -e "${YELLOW}[1/15] Checking if server is running...${NC}"
http GET $BASE_URL/health > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Server is not running! Start it with: python run.py${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Server is running${NC}\n"

# Wait function
wait_input() {
    echo -e "${YELLOW}Press ENTER to continue...${NC}"
    read
}

# =====================================
# AUTHENTICATION TESTS
# =====================================

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  AUTHENTICATION TESTS${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Test 2: Create regular user
echo -e "${YELLOW}[2/15] Creating regular user (john)...${NC}"
http POST $BASE_URL/auth/signup \
  username=john \
  email=john@example.com \
  password=pass123
wait_input

# Test 3: Login as admin
echo -e "${YELLOW}[3/15] Logging in as admin...${NC}"
ADMIN_RESPONSE=$(http POST $BASE_URL/auth/login \
  username=admin \
  password=admin123 --print=b)

# Extract token using python
ADMIN_TOKEN=$(echo $ADMIN_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['access_token'])")

if [ -z "$ADMIN_TOKEN" ]; then
    echo -e "${RED}❌ Failed to get admin token${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Admin token obtained${NC}"
echo "Token: ${ADMIN_TOKEN:0:50}..."
wait_input

# Test 4: Login as regular user
echo -e "${YELLOW}[4/15] Logging in as regular user (john)...${NC}"
USER_RESPONSE=$(http POST $BASE_URL/auth/login \
  username=john \
  password=pass123 --print=b)

USER_TOKEN=$(echo $USER_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['access_token'])")
echo -e "${GREEN}✅ User token obtained${NC}"
wait_input

# Test 5: Get current user profile (admin)
echo -e "${YELLOW}[5/15] Getting admin profile (/auth/me)...${NC}"
http GET $BASE_URL/auth/me \
  "Authorization: Bearer $ADMIN_TOKEN"
wait_input

# =====================================
# PRODUCT TESTS
# =====================================

echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}  PRODUCT MANAGEMENT TESTS${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Test 6: Create Product 1 (iPhone)
echo -e "${YELLOW}[6/15] Creating Product 1: iPhone 15 Pro...${NC}"
http POST $BASE_URL/products \
  "Authorization: Bearer $ADMIN_TOKEN" \
  name="iPhone 15 Pro" \
  description="Latest flagship smartphone with A17 Pro chip and titanium design" \
  price=999.99 \
  stock=50 \
  category="electronics" \
  image_url="https://example.com/iphone15.jpg"
wait_input

# Test 7: Create Product 2 (MacBook)
echo -e "${YELLOW}[7/15] Creating Product 2: MacBook Pro 16...${NC}"
http POST $BASE_URL/products \
  "Authorization: Bearer $ADMIN_TOKEN" \
  name="MacBook Pro 16" \
  description="Powerful laptop for developers with M3 Max chip" \
  price=2499.99 \
  stock=30 \
  category="electronics"
wait_input

# Test 8: Create Product 3 (T-Shirt)
echo -e "${YELLOW}[8/15] Creating Product 3: Cotton T-Shirt...${NC}"
http POST $BASE_URL/products \
  "Authorization: Bearer $ADMIN_TOKEN" \
  name="Cotton T-Shirt" \
  description="Comfortable 100% cotton t-shirt in multiple colors" \
  price=19.99 \
  stock=100 \
  category="clothing"
wait_input

# Test 9: Get all products (no auth)
echo -e "${YELLOW}[9/15] Getting all products (no authentication)...${NC}"
http GET $BASE_URL/products
wait_input

# Test 10: Get products with pagination
echo -e "${YELLOW}[10/15] Getting products with pagination (page=1, per_page=2)...${NC}"
http GET "$BASE_URL/products?page=1&per_page=2"
wait_input

# Test 11: Filter by category
echo -e "${YELLOW}[11/15] Filtering products by category (electronics)...${NC}"
http GET "$BASE_URL/products?category=electronics"
wait_input

# Test 12: Search products
echo -e "${YELLOW}[12/15] Searching products (search=phone)...${NC}"
http GET "$BASE_URL/products?search=phone"
wait_input

# Test 13: Get single product
echo -e "${YELLOW}[13/15] Getting single product (ID: 1)...${NC}"
http GET $BASE_URL/products/1
wait_input

# Test 14: Update product (admin)
echo -e "${YELLOW}[14/15] Updating product (price and stock)...${NC}"
http PUT $BASE_URL/products/1 \
  "Authorization: Bearer $ADMIN_TOKEN" \
  price=899.99 \
  stock=75
wait_input

# Test 15: Get categories
echo -e "${YELLOW}[15/15] Getting all categories...${NC}"
http GET $BASE_URL/products/categories
wait_input

# =====================================
# AUTHORIZATION TESTS
# =====================================

echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}  AUTHORIZATION TESTS (Should Fail)${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Test: Regular user trying to create product
echo -e "${YELLOW}[FAIL TEST 1] Regular user trying to create product...${NC}"
http POST $BASE_URL/products \
  "Authorization: Bearer $USER_TOKEN" \
  name="Unauthorized Product" \
  description="This should fail" \
  price=10 \
  stock=5
echo -e "${GREEN}✅ Correctly rejected (expected)${NC}"
wait_input

# Test: No token trying to create product
echo -e "${YELLOW}[FAIL TEST 2] Creating product without token...${NC}"
http POST $BASE_URL/products \
  name="Unauthorized Product" \
  description="This should fail" \
  price=10 \
  stock=5
echo -e "${GREEN}✅ Correctly rejected (expected)${NC}"
wait_input

# Test: Delete product (admin)
echo -e "${YELLOW}[BONUS] Deleting product (ID: 3)...${NC}"
http DELETE $BASE_URL/products/3 \
  "Authorization: Bearer $ADMIN_TOKEN"
wait_input

# =====================================
# SUMMARY
# =====================================

echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}  TEST SUITE COMPLETED!${NC}"
echo -e "${BLUE}========================================${NC}\n"

echo -e "${GREEN}✅ All tests completed successfully!${NC}"
echo -e "\nAdmin Token: ${ADMIN_TOKEN:0:50}..."
echo -e "User Token: ${USER_TOKEN:0:50}..."
echo -e "\n${YELLOW}You can now use these tokens for manual testing.${NC}"

const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');
const path = require('path');

const BASE_URL = 'http://localhost:5001/api/documents';

// Test 1: Health Check
async function testHealthCheck() {
  console.log('\n🔍 Test 1: Health Check');
  try {
    const response = await axios.get('http://localhost:5001/health');
    console.log('✅ Health check passed:', response.data);
    return true;
  } catch (error) {
    console.error('❌ Health check failed:', error.message);
    return false;
  }
}

// Test 2: Upload Document
async function testUploadDocument() {
  console.log('\n🔍 Test 2: Upload Document');
  try {
    // Create a test file
    const testFilePath = path.join(__dirname, 'test-document.txt');
    fs.writeFileSync(testFilePath, 'This is a test document for HR system');

    const formData = new FormData();
    formData.append('document', fs.createReadStream(testFilePath));
    formData.append('employeeId', 'EMP001');
    formData.append('documentType', 'resume');
    formData.append('uploadedBy', 'Test Admin');

    const response = await axios.post(`${BASE_URL}/upload`, formData, {
      headers: formData.getHeaders()
    });

    console.log('✅ Upload successful:', response.data.message);
    console.log('   Document ID:', response.data.document._id);
    
    // Cleanup
    fs.unlinkSync(testFilePath);
    
    return response.data.document._id;
  } catch (error) {
    console.error('❌ Upload failed:', error.response?.data || error.message);
    return null;
  }
}

// Test 3: Get All Documents
async function testGetDocuments() {
  console.log('\n🔍 Test 3: Get All Documents');
  try {
    const response = await axios.get(BASE_URL);
    console.log(`✅ Retrieved ${response.data.documents.length} documents`);
    return response.data.documents;
  } catch (error) {
    console.error('❌ Get documents failed:', error.message);
    return [];
  }
}

// Test 4: Get Document by ID
async function testGetDocumentById(documentId) {
  console.log('\n🔍 Test 4: Get Document by ID');
  try {
    const response = await axios.get(`${BASE_URL}/${documentId}`);
    console.log('✅ Document retrieved:', response.data.document.originalName);
    return true;
  } catch (error) {
    console.error('❌ Get document by ID failed:', error.message);
    return false;
  }
}

// Test 5: Filter Documents by Employee
async function testFilterByEmployee() {
  console.log('\n🔍 Test 5: Filter by Employee ID');
  try {
    const response = await axios.get(`${BASE_URL}?employeeId=EMP001`);
    console.log(`✅ Found ${response.data.documents.length} documents for EMP001`);
    return true;
  } catch (error) {
    console.error('❌ Filter failed:', error.message);
    return false;
  }
}

// Test 6: Get Document Versions
async function testGetVersions(documentId) {
  console.log('\n🔍 Test 6: Get Document Versions');
  try {
    const response = await axios.get(`${BASE_URL}/${documentId}/versions`);
    console.log(`✅ Document has ${response.data.versions.length} version(s)`);
    return true;
  } catch (error) {
    console.error('❌ Get versions failed:', error.message);
    return false;
  }
}

// Test 7: Delete Document
async function testDeleteDocument(documentId) {
  console.log('\n🔍 Test 7: Delete Document');
  try {
    const response = await axios.delete(`${BASE_URL}/${documentId}`);
    console.log('✅ Document deleted:', response.data.message);
    return true;
  } catch (error) {
    console.error('❌ Delete failed:', error.message);
    return false;
  }
}

// Run all tests
async function runAllTests() {
  console.log('🚀 Starting Document Management API Tests\n');
  console.log('=' .repeat(50));

  const healthOk = await testHealthCheck();
  if (!healthOk) {
    console.log('\n❌ Server is not running. Please start the server first.');
    return;
  }

  const documentId = await testUploadDocument();
  if (!documentId) {
    console.log('\n❌ Upload failed. Cannot continue tests.');
    return;
  }

  await testGetDocuments();
  await testGetDocumentById(documentId);
  await testFilterByEmployee();
  await testGetVersions(documentId);
  await testDeleteDocument(documentId);

  console.log('\n' + '='.repeat(50));
  console.log('✅ All tests completed!\n');
}

// Run tests
runAllTests().catch(console.error);

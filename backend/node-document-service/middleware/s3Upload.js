const AWS = require('aws-sdk');
const multer = require('multer');
const multerS3 = require('multer-s3');
const path = require('path');

// Configure AWS S3
const s3 = new AWS.S3({
  accessKeyId: process.env.AWS_ACCESS_KEY_ID,
  secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
  region: process.env.AWS_REGION || 'us-east-1'
});

const uploadS3 = multer({
  storage: multerS3({
    s3: s3,
    bucket: process.env.S3_BUCKET_NAME,
    acl: 'private',
    metadata: (req, file, cb) => {
      cb(null, {
        fieldName: file.fieldname,
        employeeId: req.body.employeeId,
        documentType: req.body.documentType
      });
    },
    key: (req, file, cb) => {
      const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
      cb(null, `documents/${req.body.employeeId}/${uniqueSuffix}-${file.originalname}`);
    }
  }),
  limits: { fileSize: 10 * 1024 * 1024 },
  fileFilter: (req, file, cb) => {
    const allowedTypes = /pdf|doc|docx|jpg|jpeg|png|txt|xlsx|xls/;
    const extname = allowedTypes.test(path.extname(file.originalname).toLowerCase());
    if (extname) {
      cb(null, true);
    } else {
      cb(new Error('Invalid file type'));
    }
  }
});

// Download from S3
const downloadFromS3 = async (s3Key) => {
  const params = {
    Bucket: process.env.S3_BUCKET_NAME,
    Key: s3Key
  };
  return s3.getObject(params).createReadStream();
};

// Delete from S3
const deleteFromS3 = async (s3Key) => {
  const params = {
    Bucket: process.env.S3_BUCKET_NAME,
    Key: s3Key
  };
  return s3.deleteObject(params).promise();
};

module.exports = { uploadS3, downloadFromS3, deleteFromS3, s3 };

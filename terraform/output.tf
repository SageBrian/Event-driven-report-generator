output "source_bucket_name" {
  value = aws_s3_bucket.source_bucket.id
}

output "destination_bucket_name" {
  value = aws_s3_bucket.destination_bucket.id
}
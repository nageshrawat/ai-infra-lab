output "config_file_name" {
  value = local_file.app_config.filename
}

output "environment" {
  value = var.environment
}
output "port_no" {
  value = var.port
}
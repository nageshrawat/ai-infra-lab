resource "local_file" "app_config" {
  filename = "app.conf"

  content = <<EOF
APP_NAME=${var.app_name}
ENV=${var.environment}
PORT=${var.port}
EOF
}
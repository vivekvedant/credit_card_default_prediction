

resource "null_resource" "ansible" {
   triggers  = {
      build_number = "${timestamp()}"
  }
   connection {
    type = "ssh"
    user = "ubuntu"
    private_key = "${var.pvt_key}"
    host = var.aws_instance_ip
  }

  provisioner "file" {
    source      = "ansible/playbook.yml"
    destination = "/home/ubuntu/playbook.yml"
  }
  provisioner "file" {
    source      = "ansible/install.sh"
    destination = "/home/ubuntu/install.sh"
  }
 
  provisioner "file" {
    source      = "ansible/var.yml"
    destination = "/home/ubuntu/var.yml"
  }

  provisioner "remote-exec" {
    inline = [
      "chmod +x /home/ubuntu/install.sh",
      "/home/ubuntu/install.sh",
    ]
  }
  
  # provisioner "remote-exec"{
  #   inline = ["ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook playbook.yml --extra-vars \" mongodb_url=${var.mongodb_url}  aws_account_id=${var.aws_account_id} aws_access_key=${var.aws_access_key_id} aws_region=${var.aws_default_region} aws_secret_access_key=${var.aws_secret_access_key} image_tag=${var.image_tag}\"" ]

  # }
  provisioner "remote-exec" {
    inline = [
      <<-EOT
        ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook playbook.yml \
          --extra-vars "mongodb_url=${var.mongodb_url} \
          aws_account_id=${var.aws_account_id} \
          aws_access_key=${var.aws_access_key_id} \
          aws_region=${var.aws_default_region} \
          aws_secret_access_key=${var.aws_secret_access_key} \
          image_tag=${var.image_tag}"
      EOT
    ]
  }
}
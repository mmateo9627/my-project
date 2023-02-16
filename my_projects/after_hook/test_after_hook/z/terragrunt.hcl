include {
  path = find_in_parent_folders("terragrunt.hcl")
}

dependency "clamav" {
  config_path = "../clamav"
}

terraform {
  source = "git::ssh://git@git.ac-project.net/AboveCloudDevops/infra-components/${local.component}.git//terraform?ref=${local.tag}"

  before_hook "tag_version" {
    commands = ["apply", "plan"]
    execute  = ["echo", "Current tag version:", local.tag, "Component name:", local.component]
  }

  after_hook "post_component_info" {
    commands = ["apply"]
    execute  = ["${get_parent_terragrunt_dir()}/infra-release-notification.sh", local.component, local.tag, get_aws_caller_identity_arn()]
  }

  extra_arguments "custom_vars" {
    commands = [
      "apply",
      "plan",
      "import",
      "push",
      "refresh",
      "destroy",
    ]

    arguments = [
      "-var-file=${get_parent_terragrunt_dir()}/global.tfvars",
      "-var-file=terraform.tfvars"
    ]
  }
}

inputs = {
  scanner_role_name   = dependency.clamav.outputs.scanner_role_name,
  scanner_lambda_name = dependency.clamav.outputs.scanner_lambda_name,
}

locals {
  version_vars    = read_terragrunt_config("versions.hcl")
  components_vars = read_terragrunt_config(find_in_parent_folders("components.hcl"))
  tag             = local.version_vars.locals[basename(get_terragrunt_dir())]
  component       = local.components_vars.locals[basename(get_terragrunt_dir())]
}



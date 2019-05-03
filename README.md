<!--
name: README.md
description: This file contains important information for the repository.
author: while-true-do.io
contact: hello@while-true-do.io
license: BSD-3-Clause
-->

<!-- github shields -->
[![Github (tag)](https://img.shields.io/github/tag/while-true-do/ansible-role-sys_kdump.svg)](https://github.com/while-true-do/ansible-role-sys_kdump/tags)
[![Github (license)](https://img.shields.io/github/license/while-true-do/ansible-role-sys_kdump.svg)](https://github.com/while-true-do/ansible-role-sys_kdump/blob/master/LICENSE)
[![Github (issues)](https://img.shields.io/github/issues/while-true-do/ansible-role-sys_kdump.svg)](https://github.com/while-true-do/ansible-role-sys_kdump/issues)
[![Github (pull requests)](https://img.shields.io/github/issues-pr/while-true-do/ansible-role-sys_kdump.svg)](https://github.com/while-true-do/ansible-role-sys_kdump/pulls)
<!-- travis shields -->
[![Travis (com)](https://img.shields.io/travis/com/while-true-do/ansible-role-sys_kdump.svg)](https://travis-ci.com/while-true-do/ansible-role-sys_kdump)
<!-- ansible shields -->
[![Ansible (min. version)](https://img.shields.io/badge/dynamic/yaml.svg?label=Min.%20Ansible%20Version&url=https%3A%2F%2Fraw.githubusercontent.com%2Fwhile-true-do%2Fansible-role-sys_kdump%2Fmaster%2Fmeta%2Fmain.yml&query=%24.galaxy_info.min_ansible_version&colorB=black)](https://galaxy.ansible.com/while_true_do/sys_kdump)
[![Ansible (platforms)](https://img.shields.io/badge/dynamic/yaml.svg?label=Supported%20OS&url=https%3A%2F%2Fraw.githubusercontent.com%2Fwhile-true-do%2Fansible-role-sys_kdump%2Fmaster%2Fmeta%2Fmain.yml&query=galaxy_info.platforms%5B*%5D.name&colorB=black)](https://galaxy.ansible.com/while_true_do/sys_kdump)
[![Ansible (tags)](https://img.shields.io/badge/dynamic/yaml.svg?label=Galaxy%20Tags&url=https%3A%2F%2Fraw.githubusercontent.com%2Fwhile-true-do%2Fansible-role-sys_kdump%2Fmaster%2Fmeta%2Fmain.yml&query=%24.galaxy_info.galaxy_tags%5B*%5D&colorB=black)](https://galaxy.ansible.com/while_true_do/sys_kdump)

# Ansible Role: sys_kdump

An Ansible to install and configure kdump on a host.

## Motivation

Kdump and kexec are tools often used to debug and analyze errors and crashes.

## Description

This role ensure, that kexec and kdump are properly installed and configured.

## Requirements

Used Modules:

-   [Ansible Package Module](https://docs.ansible.com/ansible/latest/modules/package_module.html)
-   [Ansible Service Module](https://docs.ansible.com/ansible/latest/modules/service_module.html)
-   [Ansible Template Module](https://docs.ansible.com/ansible/latest/modules/template_module.html)
-   [Ansible Reboot Module](https://docs.ansible.com/ansible/latest/modules/reboot_module.html)

## Installation

Install from [Ansible Galaxy](https://galaxy.ansible.com/while_true_do/sys_kdump)
```
ansible-galaxy install while_true_do.sys_kdump
```

Install from [Github](https://github.com/while-true-do/ansible-role-sys_kdump)
```
git clone https://github.com/while-true-do/ansible-role-sys_kdump.git while_true_do.sys_kdump
```

## Usage

### Role Variables

```
---
# defaults file for while_true_do.sys_kdump

wtd_sys_kdump_package:
  - kexec-tools
# State can be present|latest|absent
wtd_sys_kdump_package_state: "present"


wtd_sys_kdump_service: "kdump"
# State can be started|stopped
wtd_sys_kdump_service_state: "started"
wtd_sys_kdump_service_enabled: true

# Lookup crashkernel size
wtd_sys_kdump_crashkernel_size: "{{ lookup('file', '/sys/kernel/kexec_crash_size') }}"

# Variables for /etc/kdump.conf
# Please read templates/kdump.conf.j2
wtd_sys_kdump_conf:
  # Define the method to dump the vmcore
  # (raw|nfs|ssh|<fs type>|path)
  method: "path"
  # address or path for method
  target: "/var/crash"
  # ssh key, in case you want to use method: ssh^
  # sshkey: "/root/.ssh/kdump_id_rsa"
  # parameters for collector
  # collector: "makedumpfile -F -l --message-level 1 -d 31"
  collector: "makedumpfile -l --message-level 1 -d 31"
  # binary|script to run after vmcore dump
  # post: "/var/crash/scripts/kdump-post.sh"
  # binary|script to run before vmcore dump
  # pre: "/var/crash/scripts/kdump-pre.sh"
  # binary|script to be included in the kdump initrd
  # extra_bins: "/usr/bin/lftp"
  # extra kernel modules included in kdump initrd
  # extra_modules: "gfs2"
  # action to perform, in case kdump fails
  # (reboot|halt|poweroff|shell)
  default: "reboot"
  # specify, if initrd must be rebuild
  # (0|1)
  # force_rebuild: "1"
  # specify, if initrd must never be rebuild
  # (0|1)
  # force_no_rebuild: "1"
  # force unresettable blockdevice as target
  # (0|1)
  # override_resettable: "1"
  # extra dracut options to be inclued in initrd
  # dracut_args: '--omit-drivers "cfg80211 snd" --add-drivers "ext2 ext3"'
  # arguments for fence_kdump_send
  # fence_kdump_args: "-p 7410 -f auto -c 0 -i 10"
  # list all cluster nodes, except localhost
  # fence_kdump_nodes: "node1 node2"

# Applying new configuration to kdump needs a reboot
wtd_sys_kdump_reboot_enabled: true
wtd_sys_kdump_reboot_msg: "System is going down to apply kdump configuration."
wtd_sys_kdump_reboot_timeout: "3600"
```

### Example Playbook

Running Ansible
[Roles](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html)
can be done in a
[playbook](https://docs.ansible.com/ansible/latest/user_guide/playbooks_intro.html).

#### Simple

```
---
- hosts: all
  roles:
    - role: while_true_do.sys_kdump
```

#### Advanced

Use an nfs address as target.

```
- hosts: all
  roles:
    - role: while_true_do.sys_kdump
      wtd_sys_kdump_conf
        method: "nfs"
        target: "192.168.10.1:/path/to/dir"
```

## Known Issues

1.  Testing RedHat is currently only possible with a valid subscription.
    For now, RedHat Testing is faked via CentOS.
2.  Grub is not configured by this role.

## Testing

Most of the "generic" tests are located in the
[Test Library](https://github.com/while-true-do/test-library).

Ansible specific testing is done with
[Molecule](https://molecule.readthedocs.io/en/stable/).

Infrastructure testing is done with
[testinfra](https://testinfra.readthedocs.io/en/stable/).

Automated testing is done with [Travis CI](https://travis-ci.com/while-true-do).

## Contribute

Thank you so much for considering to contribute. We are very happy, when somebody
is joining the hard work. Please fell free to open
[Bugs, Feature Requests](https://github.com/while-true-do/ansible-role-sys_kdump/issues)
or [Pull Requests](https://github.com/while-true-do/ansible-role-sys_kdump/pulls) after
reading the [Contribution Guideline](https://github.com/while-true-do/doc-library/blob/master/docs/CONTRIBUTING.md).

See who has contributed already in the [kudos.txt](./kudos.txt).

## License

This work is licensed under a [BSD-3-Clause License](https://opensource.org/licenses/BSD-3-Clause).

## Contact

-   Site <https://while-true-do.io>
-   Twitter <https://twitter.com/wtd_news>
-   Code <https://github.com/while-true-do>
-   Mail [hello@while-true-do.io](mailto:hello@while-true-do.io)
-   IRC [freenode, #while-true-do](https://webchat.freenode.net/?channels=while-true-do)
-   Telegram <https://t.me/while_true_do>

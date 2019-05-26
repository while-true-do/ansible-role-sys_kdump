import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_kdump_pkg(host):
    vrt = host.ansible("setup")["ansible_facts"]["ansible_virtualization_type"]
    if vrt != 'docker':
        pkg = host.package('kexec-tools')

        assert pkg.is_installed


def test_kdump_conf(host):
    vrt = host.ansible("setup")["ansible_facts"]["ansible_virtualization_type"]
    if vrt != 'docker':
        file = host.file('/etc/kdump.conf')

        assert file.exists


def test_kdump_srv(host):
    vrt = host.ansible("setup")["ansible_facts"]["ansible_virtualization_type"]
    if vrt != 'docker':
        srv = host.service('kdump')

        assert srv.is_running
        assert srv.is_enabled

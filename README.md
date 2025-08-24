Test Infrastructure Template
============================

This is an IaC template for provisioning a locally hosted virtual
infrastructure. The project simplifies deployment of infrastructures for testing
and prototyping.

Key features:

- IaC configuration
- network topologies with multiple networks are supported
- cloud image ready
- VirtualBox backed
- Ansible based provisioning
- [Task][Task] based framework

[Task]: https://taskfile.dev/

Cloud image requirements:

- QCOW2 format
- cloud-init is installed
- virtio storage and network drivers are installed

Requirements
------------

- macOS or Linux host
- [Task](https://taskfile.dev/docs/installation)
- [Python 3](https://docs.python.org/3/using/index.html)
- [VirtualBox](https://www.virtualbox.org/manual/ch02.html)
- [yq](https://github.com/mikefarah/yq)
- [curl](https://curl.se/download.html)
- [QEMU](https://www.qemu.org/download/) — only the `qemu-img` utility is used
  (converting cloud images from QCOW2 to VDI)
- OpenSSH client

Quick Start
-----------

Example infrastructure:

```
+--------------------------------------------+
|                 VirtualBox                 |
|    NAT network              NAT network    |
|    =====+=====              =====+=====    |
|         |                        |         |
| +-------+----------+  +----------+-------+ |
| | instance "alice" |  |  instance "bob"  | |
| +---------------+--+  +--+---------------+ |
|  192.168.100.10 |        | 192.168.100.20  |
|                 |        |                 |
|   ==============+========+==============   |
|   internal network "test-infrastructure"   |
|              192.168.100.0/24              |
+--------------------------------------------+
```

**Note.** This example is configured for amd64 hosts. For arm64 (Apple silicon)
hosts update `infrastructure.yml` and `ansible/inventory/hosts.yml` files
according to the instructions in comments.

Create VirtualBox infrastructure (instances and networks):

```sh
task create
```

Start instances:

```sh
task start
```

Provision instances with Ansible:

```sh
task ansible-requirements
task provision
```

Use infrastructure:

```sh
. ansible/venv/bin/activate
curl --head http://127.0.0.1:20080/
ansible --args='ip address show' infrastructure
ssh -F ssh/config alice ping -c 5 192.168.100.20
```

Power off instances:

```sh
task poweroff
```

Delete VirtualBox infrastructure, source QCOW2 images, Ansible requirements:

```sh
task delete-all
```

Template Customization
----------------------

For basic customizations:

- `infrastructure.yml` — VirtualBox infrastructure configuration
- `ansible/inventory/hosts.yml` — Ansible inventory
- `ansible/playbooks/provision.yml` — Ansible playbook runned
  by the `task provision` command
- `ansible/requirements.txt` — Python packages installed
  by the `task ansible-requirements` command
- `ansible/requirements.yml` — Ansible collections and roles installed
  by the `task ansible-requirements` command

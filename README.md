# Ansible Notes

## Overview

Inventory file:
* hosts:
  * ansible-web01
  * ansible-web02
  * ansible-db01
* Inventory Host var for private ssh key file
* Inventory Group var for ansible_user=vagrant

## Ansible from Commandline

```bash
# check connectivity
ansible all -i hosts -m ping
# Facts
ansible db -i hosts -m setup
# Install Apache (as root) - repeat shows idempotent
ansible ansible-web01 -i hosts -m yum -a "name=httpd state=present" -b
# remove package
ansible ansible-web01 -i hosts -m yum -a "name=httpd state=absent" -b
```

## All-in-one playbook

a1_playbook:
* Uses variable to install multiple items
* Runs getenforce & captures output into variable sestatus
* Installs Apache and starts the service

```bash
ansible-playbook -i hosts a1_playbook.yml
```

## Roles

Example roles at <http://galaxy.ansible.com>

`site.yml` playbook:
* Targets hosts with roles

```bash
# Create two roles
mkdir roles; cd roles
ansible-galaxy init common
ansible-galaxy init apache
```

Common tasks, handlers and template files:
* (new) `roles/common/tasks/selinux.yml`
* (new) `roles/common/tasks/ntp.yml`
* (mod) `roles/common/handlers/main.yml`
* (new) `roles/common/tempates/ntp.conf.j2`
  * Has ntpserver variable
* (new) `group_vars/all`
  * New dir and file
  * Contains ntpserver value
* (mod) `roles/common/tasks/main.yml`
  * put in epel repo

Files only have sequence sections for type. E.g. task sequences only

Apache role files:
* (mod) `roles/apache/tasks/main.yml`
  * Uses variable for apache_dirs
  * Uses var for dest apache_docroot
  * Uses var to select template based on OS family
* (new) `roles/apache/templates/httpd.conf-RedHat.j2`
* (new) `roles/apache/templates/index.html.j2`
  * Displays ansible_distribution and host names from the webservers group
* (mod) `roles/apache/handlers/main.yml`
  * Add restart apache handler
* (new) `group_vars/webservers`
  * Vars for apache etc

## Web Role - Built on other roles

```bash
cd roles
ansible-galaxy init web
```

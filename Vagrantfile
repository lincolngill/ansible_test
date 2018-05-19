# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "links/centos7"
  config.vm.provider "virtualbox" do |v|
    v.memory = 1024
    v.cpus = 1
    v.linked_clone = true
  end

  config.vm.provision "bootstrap", type: "shell" do |s|
    s.inline = "yum -y update"
  end

  config.vm.define "web01" do |web01|
    web01.vm.hostname = "ansible-web01.homelan.co.nz"
    web01.vm.network "private_network", ip: "192.168.33.10"
  end

  config.vm.define "web02" do |web02|
    web02.vm.hostname = "ansible-web02.homelan.co.nz"
    web02.vm.network "private_network", ip: "192.168.33.20"
  end

  config.vm.define "db01" do |db01|
    db01.vm.hostname = "ansible-db01.homelan.co.nz"
    db01.vm.network "private_network", ip: "192.168.33.30"
  end

end

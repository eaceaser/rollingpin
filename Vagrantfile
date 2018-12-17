Vagrant.configure(2) do |config|
  config.vm.box = "puppetlabs/ubuntu-16.04-64-puppet"
  config.vm.box_version = "1.0.0"
  config.vm.network "private_network", type: "dhcp"
  config.vm.hostname = "rollingpin.local"

  config.vm.provision :shell, inline: "apt-get update && apt-get install -y software-properties-common"
  config.vm.provision :puppet do |puppet|
    puppet.manifests_path = "./puppet"
    puppet.manifest_file = "init.pp"
    puppet.module_path = "./puppet/modules"
    puppet.facter = {
      "user" => "vagrant",
      "project_path" => "/home/vagrant/rollingpin",
    }
  end

  config.vm.synced_folder  ".", "/home/vagrant/rollingpin"
end

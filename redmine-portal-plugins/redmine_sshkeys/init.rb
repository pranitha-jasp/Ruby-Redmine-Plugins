require 'redmine'

Redmine::Plugin.register :redmine_sshkeys do
  name 'Redmine Sshkeys plugin'
  author 'Vamsi Krishna B, Swetha V'
  description 'This is a plugin for Redmine'
  version '0.0.1'
  
  permission :view_key, { :sshkeys => [:index] }, :public => true
#  permission :edit_releases, { :releases => [:new, :publish] }
  
  
  menu :project_menu, :sshkeys, { :controller => 'sshkeys', :action => 'index' }, :after => :activity, :caption => 'SSH-Keys', :param => :project_id
end

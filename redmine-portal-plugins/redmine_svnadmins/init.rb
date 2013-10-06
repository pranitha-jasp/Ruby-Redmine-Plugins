require 'redmine'

Redmine::Plugin.register :redmine_svnadmins do
  name 'Redmine Svnadmins plugin'
  author 'Vamsi Krishna B, Swetha V'
  description 'This is a plugin for Redmine'
  version '0.0.1'
  
  permission :new_repo, { :svnadmins => [:new] }
  permission :view_svn, { :svnadmins => [:index]}, :public => true
  
  
  menu :project_menu, :svnadmins, { :controller => 'svnadmins', :action => 'index' }, :caption => 'SVN Admin', :after => :sshkeys, :param => :project_id

end

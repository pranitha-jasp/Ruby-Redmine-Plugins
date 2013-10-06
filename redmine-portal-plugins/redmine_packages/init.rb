require 'redmine'

Redmine::Plugin.register :redmine_packages do
  name 'Redmine Packages plugin'
  author 'Vamsi Krishna B, Swetha V'
  description 'This is a plugin for Redmine'
  version '0.0.1'
  
  permission :view_package, { :packages => [:index] }, :public => true
  permission :new_package, { :packages => [:new] }
  permission :reload_package, { :packages => [:reload] }
    
  menu :project_menu, :packages, { :controller => 'packages', :action  => 'index' }, :caption => 'Server-Side Requirements', :after => :activity, :param => :project_id

end

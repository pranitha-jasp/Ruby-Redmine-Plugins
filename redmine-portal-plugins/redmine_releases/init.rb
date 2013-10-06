require 'redmine'

Redmine::Plugin.register :redmine_releases do
  name 'Redmine Releases plugin'
  author 'Swetha V'
  description 'This is a plugin for Redmine'
  version '0.0.1'

  permission :view_releases, { :releases => [:index] }, :public => true
  permission :edit_releases, { :releases => [:new, :publish] }
  
  permission :releases, { :releases => [:index] }, :public => true
  menu :project_menu, :releases, { :controller => 'releases', :action => 'index' }, :caption => 'Releases', :after => :packages, :param => :project_id

end

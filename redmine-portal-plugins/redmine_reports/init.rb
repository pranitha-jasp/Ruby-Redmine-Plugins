require 'redmine'

Redmine::Plugin.register :redmine_reports do
  name 'Redmine Reports plugin'
  author 'Vamsi Krishna B & Swetha V'
  description 'This is a plugin for Redmine'
  version '0.0.1'
  permission :view_report, { :feedbackreports => [:index] }, :public => true

  menu :project_menu, :reports, { :controller => 'feedbackreports', :action => 'index' }, :caption => 'Feedback Reports', :after => :releases, :param => :project_id
end

class SshkeysController < ApplicationController
  menu_item :sshkey
  menu_item :settings, :only => :edit
  helper :projects
  
  unloadable
  def index
    @project = Project.find(params[:project_id])
    if !( @project && User.current.allowed_to?(:view_key, @project))
      render_403
      return
    end
    @currentkey = nil
    Sshkey.find(:all).each do |@key|
      if @key[:username] == User.current.login
        @currentkey = @key
      end
    end
    
    if request.post?
      if @currentkey
        @currentkey.delete
      end
      @currentkey = Sshkey.new()
      @currentkey.username = User.current.login
      @currentkey.key = params[:sshkey][:key]
      response = @currentkey.update(User.current.login,params[:sshkey][:key])
      if response['status'] == 1
        @currentkey.save
        flash[:notice] = "Key Updated Successfully. It might take some time(5-10min) for getting an access to the svn server"
      else
        flash[:error] = "Update failed: "+ response['summary']
	redirect_to :controller => 'sshkeys', :action => 'index', :project_id => params[:project_id]
      end
    end
  end
end

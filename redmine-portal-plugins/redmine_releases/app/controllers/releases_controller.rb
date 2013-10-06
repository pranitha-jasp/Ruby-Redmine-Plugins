class ReleasesController < ApplicationController
  unloadable
  helper :sort
  include SortHelper

  def index
    sort_init 'Sno', 'asc'
    sort_update 'Sno' => "id",
    'Repo Name' => "#{Release.table_name}.url",
    'SVN Revision' => "#{Release.table_name}.revision",
    'Previewed_On' => "#{Release.table_name}.is_previewed",
    'Published_On' => "#{Release.table_name}.is_published",
    'Repo Type' => "#{Release.table_name}.repo_type"
    @project = Project.find(params[:project_id])
    @releases = Release.find(:all, :order => sort_clause) # @project.releases                      
  end
  
  def new
    # Submit a new release with repo URL and revision                                              
    @project = Project.find(params[:project_id])
    # Preview page is editable only by the current user                                            
    if !( @project && User.current.allowed_to?(:edit_releases, @project))
      render_403
      return
    end
    
    @release = Release.new()
    if request.post?
      @release.url = params[:release][:url]
      @release.revision = params[:release][:revision]
      @release.lab_id = params[:release][:project_id]
      @release.repo_type = params[:release][:repo_type]
      if @release.save
        # do nothing                                                                               
        flash[:notice] = "Please wait...."
      else
        flash[:error] = "Please check supplied data"
        return
      end
      # Preview a release i.e. move your lab to test machine                                       
      response = @release.test(params[:release][:project_id],params[:release][:url],params[:release][:revision],params[:release][:repo_type])
      flash.discard
      if response['status'] == 1
        @release.is_previewed = Time.now.strftime("%Y-%m-%d %H:%M")
        flash[:notice] = "Test successful"
      else
        @release.is_previewed = "None"
        @release.delete
        redirect_to :controller => 'releases', :action => 'index', :project_id => params[:release][:project_id]
        flash[:error] = "Test failed: "+ response['error']
        return
      end
      @release.summary = response['summary']
      @release.time = Time.now.strftime("%Y-%m-%d %H:%M")

      if @release.save
        redirect_to :controller => 'releases', :action => 'index', :project_id => params[:release][:project_id]
      else
        flash[:error] = "OOPS! something went wrong"
      end
    end
  end
  
  def publish
    # Find recent and successful preview and publish it                                             
    @project = Project.find(params[:project_id])
    if !( @project && User.current.allowed_to?(:edit_releases, @project))
      render_403
      return
    end
    @lab_releases = []
    @releases = Release.find(:all)
    if request.post?
      @releases.each do |release|
        if release.lab_id == params[:project_id]
          @lab_releases.insert(0,release)
        end
      end
      #  @lab_releases.sort! { |a,b| a.id <=> b.id }                                               
      # Publishes your lab i.e your lab in on deploy machine                                       
      @lab_releases.each do |@lab_release|
        if @lab_release.is_previewed != 'None'
          @lab_release.publish(params[:project_id])
          @lab_release.is_published = Time.now.strftime("%Y-%m-%d %H:%M")
          if @lab_release.save
            redirect_to :controller => 'releases', :action => 'index', :project_id => params[:project_id]
            flash[:notice] = "Release Successful"
            return
          else
            flash[:error] = "Release Failed"
          end
        end
      end
    end
  end
  def clear
    @project = Project.find(params[:project_id])
    if !( @project && User.current.allowed_to?(:edit_releases, @project))
      render_403
      return
    end
    @releases = Release.find(:all)
    if request.post?
      @releases.each do |release|
        if release.lab_id == params[:project_id] and release.is_published == nil
          release.delete
        end
      end
      redirect_to :controller => 'releases', :action => 'index', :project_id => params[:project_id]
      flash[:notice] = "Cleared all the unreleased instances"
      return
    end
  end
end

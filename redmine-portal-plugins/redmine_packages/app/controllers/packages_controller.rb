
ActiveResource::Base.logger = Logger.new(STDOUT)
ActiveResource::Base.logger.level = Logger::DEBUG

def debug(msg)
ActiveResource::Base.logger.debug(msg)
end



class PackagesController < ApplicationController
  helper :sort
  include SortHelper
  verify :method => :post, :only => :destroy
  def index
    sort_init 'Sno', 'asc'
    sort_update 'Sno' => "id",
    'Package Name' => "#{Package.table_name}.packagename",
    'Version' => "#{Package.table_name}.version",
    'Status' => "#{Package.table_name}.status"
    @project = Project.find(params[:project_id])
    @packages = Package.find(:all, :order => sort_clause)
  end
  def new
    @project = Project.find(params[:project_id])
    if !( @project && User.current.allowed_to?(:new_package, @project))
      render_403
      return
    end
    
    if request.post?
      @packages = Package.find(:all)
      @packages.each do |@package|
        if @package.packagename == params[:package][:packagename] and @package.lab_id == params[:project_id]
          redirect_to :controller => 'packages', :action => 'index', :project_id => params[:project_id]
          flash[:notice] = "Package already exists"
          return
        end
      end
      @package = Package.new()
      @package.packagename = params[:package][:packagename]
      @package.lab_id = params[:project_id]
      @package.status = "Processing"
      status = @package.add(@package.lab_id,@package.packagename)
      if @package.save 
        redirect_to :controller => 'packages', :action => 'index', :project_id => params[:project_id]
        flash[:notice] = "Package will be installed. Refresh status after some time."
        return
      else
        redirect_to :controller => 'packages', :action => 'index', :project_id => params[:project_id]
        flash[:error] = "Check the package name."
        return
      end
    end  
  end
  
  def destroy
    @project = Project.find(params[:project_id])
    @packages = Package.find(:all)
    if request.post?
      @packages.each do |@package|
        if params[:project_id] == @package.lab_id and params[:package] == @package.packagename
          status = @package.drop(@package.lab_id,@package.packagename)
          redirect_to :controller => 'packages', :action => 'index', :project_id => params[:project_id]
          
          name = @package.packagename
          @package.delete
          flash[:notice] = name +" is no longer monitored"
          return
        end
      end
    end
  end
  
  def reload
    @project = Project.find(params[:project_id])
    package_name = params[:package]
    @packages = Package.find(:all)
    @package = Package.find(:first)
    status = @package.getstatus(params[:project_id],package_name)
    debug(status) 	    
    if request.post?
      if package_name == 'all'
        @packages.each do |@package|
          @package.status = status[@package.packagename]['status']
          @package.version = status[@package.packagename]['version']      
          if @package.status == 'Installed'
            @package.save
          end
        end
      else
        @packages.each do |@package|
          if @package.packagename == package_name
            @package.status = status['status'] 
            @package.version = status['version']      
            if @package.status == 'Installed'
              @package.save
              debug("Status: "+status['status'])
            end
          end
        end  
        redirect_to :controller => 'packages', :action => 'index', :project_id => params[:project_id] 	    
        return 
      end
    end
  end
end


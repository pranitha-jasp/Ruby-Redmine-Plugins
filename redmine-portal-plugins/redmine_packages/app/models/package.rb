
ActiveResource::Base.logger = Logger.new(STDOUT)
ActiveResource::Base.logger.level = Logger::DEBUG

def debug(msg)
ActiveResource::Base.logger.debug(msg)
end

class Package < ActiveRecord::Base
  validates_presence_of :packagename
  validates_format_of :packagename, :with => /^[^ ]+$/
  def command(name,lab_id,packagename)
    sub_cmd = "~/pacman.py "+name+" "+packagename+" "+lab_id
    command = 'ssh tester@devel "'+sub_cmd+'"'
    response = `#{command}`
    j = ActiveSupport::JSON
    response = j.decode(response)
  end
  def getstatus(lab_id, packagename)
    command('status',lab_id,packagename)
  end

  def add(lab_id, packagename)
    command('add',lab_id,packagename)
  end
  
  def drop(lab_id,packagename)
    command('drop',lab_id,packagename)
  end

end

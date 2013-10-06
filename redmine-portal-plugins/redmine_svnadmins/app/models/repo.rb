
class Repo < ActiveRecord::Base
  
  validates_presence_of :reponame
  validates_presence_of :description
  
  def manage(action,lab_id, reponame)
    sub_cmd = "~/svnadmin.py "+action+" "+lab_id+" "+reponame
    command = 'ssh svnadmin@devel "'+sub_cmd+'"'
    response = `#{command}`
    j = ActiveSupport::JSON
    response = j.decode(response)
  end
  
end

require 'open3'

class Release < ActiveRecord::Base
  
  belongs_to :author, :class_name => "User", :foreign_key => "author_id"
  
  validates_presence_of :url

  #validates_numericality_of :revision, :only_integer => true, :message => "can only be whole number."
                                                                                                
  #validates_format_of :revision, :with => /^\w+$/i                                                
  
  def test (project_id, repo, revision, repo_type)
    sub_cmd = "~/push2test_test.py "+repo_type+" "+project_id+" "+repo+" "+String (revision)
    command = 'ssh tester@devel "'+sub_cmd+'"'
    response = `#{command}`
    j = ActiveSupport::JSON
    response = j.decode(response)
  end

  def publish (project_id)
    sub_cmd = "~/publish.py "+project_id
    command = 'ssh tester@devel "'+sub_cmd+'"'
    `#{command}`
    "Yes"
  end

end


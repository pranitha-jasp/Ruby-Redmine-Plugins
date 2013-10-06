class Sshkey < ActiveRecord::Base
  belongs_to :project
  
 
  validates_presence_of :key
  validates_format_of :key, :with => /^ssh\-[a-zA-Z0-9 +]*[@=\/$]*[a-zA-Z0-9\-]*/
  def update (username, key)
    sub_cmd = "~/updatekey.py "+username+" "+key
    command = 'ssh importer@devel "'+sub_cmd+'"'
    response = `#{command}`
    j = ActiveSupport::JSON
    response = j.decode(response)
  end

end

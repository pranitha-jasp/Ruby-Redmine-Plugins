class CreateSshkeys < ActiveRecord::Migration
  def self.up
    create_table :sshkeys do |t|
      t.column :username, :string
      t.column :key, :string
    end
  end

  def self.down
    drop_table :sshkeys
  end
end

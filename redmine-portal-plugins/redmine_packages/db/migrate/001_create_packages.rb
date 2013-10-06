class CreatePackages < ActiveRecord::Migration
  def self.up
    create_table :packages do |t|
      t.column :lab_id, :string
      t.column :packagename, :string
      t.column :status, :string
      t.column :version, :string
    end
  end

  def self.down
    drop_table :packages
  end
end

class CreateReleases < ActiveRecord::Migration
  def self.up
    create_table :releases do |t|
      t.column :lab_id, :string
      t.column :url, :string
      t.column :revision, :string
      t.column :summary, :string
      t.column :is_previewed, :datetime
      t.column :is_published, :datetime
      t.column :time, :datetime
      t.column :repo_type, :string
    end
  end

  def self.down
    drop_table :releases
  end
end

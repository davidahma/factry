# frozen_string_literal: true

require 'pathname'
require 'yaml'

root = Pathname.new(__dir__).parent.realpath
Dir.chdir(root)
linked = ['skills', *Dir.glob('skills/**/*', File::FNM_DOTMATCH)].find { |path| File.symlink?(path) }
abort "Skills must contain portable files: #{linked}" if linked
skills = Dir.glob('skills/*').sort
abort 'Missing skills' if skills.empty?
listed = File.readlines('scripts/skill-catalog.txt').map(&:chomp)
abort 'Release catalog and skill directories differ' unless listed == skills.map { |path| File.basename(path) }
catalog = File.read('README.md', encoding: 'UTF-8')

skills.each do |folder|
  name = File.basename(folder)
  file = File.join(folder, 'SKILL.md')
  abort "Missing skill entry point: #{file}" unless File.file?(file)
  parts = File.read(file, encoding: 'UTF-8').match(/\A---\n(.*?)\n---\n(.+)\z/m)
  abort "Invalid skill file: #{file}" unless parts && !parts[2].strip.empty?
  fields = YAML.safe_load(parts[1])
  abort "Invalid name: #{file}" unless fields.is_a?(Hash) && fields['name'] == name &&
    name.match?(/\Afactry-[a-z0-9]+(?:-[a-z0-9]+)*\z/) && name.size <= 64
  description = fields['description']
  abort "Invalid description: #{file}" unless description.is_a?(String) &&
    description.strip.size.between?(1, 1024)
  abort "Missing README entry: #{name}" unless catalog.include?("](#{file})")
end

# This repository uses inline Markdown links for local files.
Dir.glob('**/*.md', File::FNM_DOTMATCH).each do |file|
  next if file.start_with?('.git/')
  File.read(file, encoding: 'UTF-8').scan(/\]\(([^()\s]+)\)/).flatten.each do |link|
    next if link.start_with?('https://', 'http://', '#', 'mailto:')
    path = link.split('#', 2).first
    target = root.join(File.dirname(file), path).cleanpath
    allowed = file.start_with?('skills/') ? root.join(*file.split('/').first(2)) : root
    unless target.exist? && (target.realpath == allowed || target.realpath.to_s.start_with?(allowed.to_s + '/'))
      abort "Broken or nonportable link in #{file}: #{link}"
    end
  end
end

puts "#{skills.size} skill manifests, catalog entries, and local file links passed."

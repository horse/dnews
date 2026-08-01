#!/usr/bin/env ruby
# frozen_string_literal: true

edition_date = ENV['EDITION_DATE']
command = ['python3', 'tools/validate_edition.py']
if edition_date && !edition_date.empty?
  command.concat(['--edition-date', edition_date])
else
  command << '--all'
end
exec(*command)

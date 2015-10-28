require 'sinatra'

set :port, 8080
set :static, true
set :public_folder, "static"
set :views, "views"

get '/' do
    erb :index, :locals => {'params' => params}
end

get '/load/' do
	if not params[:graph].nil? then
		graphfile = "data/" + params[:graph] + ".graph.json"
		file = File.open( graphfile, "rb")
		graph = file.read
    	return graph
	end
	if not params[:nodes].nil? then
		nodefile = "data/" + params[:nodes] + ".nodes.json"
		file = File.open(nodefile, "rb")
		nodes = file.read
    	return nodes
	end
	return "Error"
end

post '/save/' do
	if not params[:graph].nil? and not params[:data].nil? then
		graphfile = "data/" + params[:graph] + ".graph.json"
		File.open(graphfile, 'w') { |file| file.write(params[:data]) }
    	return "Success"
	end
	return "Error"
end

get '/save/' do
	if not params[:graph].nil? and not params[:data].nil? then
		graphfile = "data/" + params[:graph] + ".graph.json"
		File.open(graphfile, 'w') { |file| file.write(params[:data]) }
    	return "Success"
	end
	return "Error"
end
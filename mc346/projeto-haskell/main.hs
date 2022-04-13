import System.IO
import System.Environment     
import Data.List

data Aresta = Aresta {
    origem::String,
    destino::String,
    metodo::String,
    peso:: Float
} deriving (Eq,Show,Read)

data No = No {
    nome::String,
    arestas::[Aresta]
} deriving (Eq,Show,Read)

data Grafo = Grafo {
    nos::[No]
} deriving (Eq,Show,Read)

data TempoDeEspera = TempoDeEspera {
    tempo::Float,
    linha::String
} deriving (Eq,Show,Read)

getNodes :: [String] -> [No]
getNodes l = cleanDuplicates (foldr (\it rest -> it ++ rest) [] (map (\it -> lineToNode (words it)) (filterLines l)))
    where
        filterLines ([]:xs) = []
        filterLines (x:xs) = (x :(filterLines xs))
        lineToNode [origin, destination, _, _] = [
            No {
                nome = origin,
                arestas = []
            },
            No {
                nome = destination,
                arestas = []
            }]
        cleanDuplicates [] = []
        cleanDuplicates (x:xs) = (x:(cleanDuplicates (foldr (\it rest -> if it == x then rest else (it:rest))[] xs)))

getLinks :: [No] -> [String] -> [No]
getLinks nodes l = map (\it -> addEdgesToNode (createEdges l) it) nodes
    where
        createEdges l = (map (\it -> lineToEdge (words it)) (filterLines l))
        filterLines ([]:xs) = []
        filterLines (x:xs) = (x :(filterLines xs))
        addEdgesToNode edges node = foldl (\n it -> addEdgeToNode it n) node edges
        addEdgeToNode (Aresta {origem = origin, destino = destination, metodo = method, peso = length}) (No {nome = nome, arestas = arestas})
          | nome == origin = No {
            nome = nome,
            arestas = (Aresta {
              origem = origin,
              destino = destination,
              metodo = method, 
              peso = length
            }:arestas)
          }
          | otherwise = No {nome = nome, arestas = arestas}  
        lineToEdge [origin, destination, method, length] = Aresta {
            origem = origin,
            destino = destination,
            metodo = method, 
            peso = read length :: Float
        }

getWaitingTimes :: [String] -> [TempoDeEspera]
getWaitingTimes l = (map (\it -> lineToWaitingTime (words it)) (removeAfterEmpty (removeBeforeEmpty l)))
        where         
            removeAfterEmpty ([]:xs) = [] 
            removeAfterEmpty (x:xs) = (x :(removeAfterEmpty xs))
            removeBeforeEmpty ([]:xs) = xs
            removeBeforeEmpty (_:xs) = (removeBeforeEmpty xs)
            lineToWaitingTime [line, time] = TempoDeEspera {
                linha=line,
                tempo= read time :: Float
            }

getOriginDestination :: [String] -> (String, String)
getOriginDestination l = lineToOriginDestination (words (head (removeBeforeEmpty (removeBeforeEmpty l))))
            where
                removeBeforeEmpty :: [String] -> [String]
                removeBeforeEmpty ([]:xs) = xs
                removeBeforeEmpty (_:xs) = (removeBeforeEmpty xs)
                lineToOriginDestination [origin, destination] = (origin, destination)

getNodeByName :: [No] -> String -> No
getNodeByName nodes name = foldr (\it rest -> if name == (nome it) then it else rest) No{nome="not found", arestas=[]} nodes

notPassed :: [No] -> No -> Bool
notPassed passedNodes node = foldr (\it rest -> if it == node then False else rest) True passedNodes

filteredLinks :: [No] -> [Aresta] -> [No] -> [Aresta]
filteredLinks _ [] _ = []
filteredLinks nodes (x:xs) passed =  if (notPassed passed (getNodeByName nodes (origem x))) then (x:(filteredLinks nodes xs passed)) else (filteredLinks nodes xs passed)

flatten :: [[[Aresta]]] -> [[Aresta]]
flatten [] = []
flatten (x:xs) = x ++ (flatten xs)

getPossiblePaths :: Grafo -> String -> String -> [[Aresta]]
getPossiblePaths Grafo { nos=nos } origin destination = getPossiblePaths' nos (getNodeByName nos origin) destination []
            where
                addOrigin :: Aresta -> [[Aresta]] -> [[Aresta]]
                addOrigin link paths = map (\path -> (link:path)) paths 
                getPossiblePaths' :: [No] -> No -> String -> [No] -> [[Aresta]]
                getPossiblePaths' nodes origin destination passed
                    | (nome origin) == destination = [[]]
                    | flinks == [] = []
                    | otherwise = flatten (
                        map (\it -> 
                            let p = (getPossiblePaths' nodes (getNodeByName nodes (destino it)) destination (origin:passed)) in
                            addOrigin it p
                            ) flinks
                    )
                    where 
                        flinks = (filteredLinks nodes (arestas origin) passed)

getWaitingTime :: String -> [TempoDeEspera] -> Float              
getWaitingTime _ [] = 0
getWaitingTime method ((TempoDeEspera {tempo = time, linha = l}):tempos)
    | method == l = 0.5*time
    | otherwise = getWaitingTime method tempos

getTotalTime :: [Aresta] -> [TempoDeEspera] -> Float
getTotalTime [] waitingTimes = 0.0
getTotalTime [(Aresta {origem = origin, destino = destination, metodo = method, peso = length})] waitingTimes =
    if (isInfixOf "linha" method) then (getWaitingTime method waitingTimes) + length else length
getTotalTime ((Aresta {origem = origin, destino = destination, metodo = method, peso = length}):arestas) waitingTimes = (if (isInfixOf "linha" method) then (getWaitingTime method waitingTimes) + length else length) + (getTotalTime' method arestas waitingTimes)
    where
        getTotalTime' :: String -> [Aresta] -> [TempoDeEspera] -> Float
        getTotalTime' _ [] waitingTimes = 0.0
        getTotalTime' ant ((Aresta {origem = origin, destino = destination, metodo = method, peso = length}):arestas) waitingTimes
            | (isInfixOf "linha" method) && (ant /= method) = (getWaitingTime method waitingTimes) + length + (getTotalTime' method arestas waitingTimes)
            | otherwise = length + (getTotalTime' method arestas waitingTimes)
  
getShortestTime :: [[Aresta]] -> [TempoDeEspera] -> Float
getShortestTime (path:paths) waitingTimes = foldl (\acc it -> if (getTotalTime it waitingTimes) < acc then (getTotalTime it waitingTimes) else acc) (getTotalTime path waitingTimes) paths

getShortestPath :: [[Aresta]] -> [TempoDeEspera] -> [Aresta]
getShortestPath (path:paths) waitingTimes = foldl (\acc it -> if (getTotalTime it waitingTimes) < (getTotalTime acc waitingTimes) then it else acc) path paths

pathToString :: [Aresta] -> String
pathToString path = (origem (head path)) ++ " " ++ foldr(\Aresta {destino=destino, metodo=metodo} rest -> metodo ++ " " ++ destino ++ " " ++ rest) "" path

main = do 
    -- contents <- readFile "in.in"
    contents <- getContents
    let l = lines contents
    let nodes = getNodes l
    let waitingTimes = getWaitingTimes l
    let graph =  Grafo { nos = getLinks nodes l}

    let originDestination = getOriginDestination l
    let possiblePaths = getPossiblePaths graph (fst originDestination) (snd originDestination)
    let shortestTime = getShortestTime possiblePaths waitingTimes
    let shortestPath = getShortestPath possiblePaths waitingTimes

    
    putStrLn (pathToString shortestPath)
    putStrLn (show shortestTime)
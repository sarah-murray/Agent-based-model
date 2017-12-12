import random

class Agent():
    """
    Provide methods to create an agent based model.
    
    Build agents and allow them to move within an environment. Allow 
    agents to take data from the environment and share with each
    other.
    """

    #__init__ defines agents, gives access to DEM and agent information
    def __init__ (self, environment, agents, y, x):
        """
        Define an agent at a location within the environment.
        
        If location data not available, provide random coordinates for 
        agent between 0-99.
        
        Args:
            environment (int, float) -- environmental data as .csv
            agents (int) -- information associated with other agents in
                the environment
            y (int) -- existing y coordinate 
            x (int) -- existing x coordinate
        
        Returns:
            y (int) -- random y coordinate between 0-99
            x (int) -- random x coordinate between 0-99

            
        """
        #if no x coordinate available, create a random number between 0-99
        if (x == None):
            self.x = random.randint (0, 99)
        #otherwise use available x
        else:
            self.x = x
        #if no x coordinate available, create a random number between 0-99
        if (y == None):
            self.y = random.randint (0, 99)
        #otherwise use available x
        else:
            self.y = y
        self.environment = environment
        self.agents = agents
        self.store = 0

    #Moves an agent a single step and keeps within the grid
    def move(self):
        """
        Move agent within the environment.
        
        Assign direction of travel randomly and move 1 space. Keep agent
        within the environment using a torus boundary effect.
        
        Requires no setup.
        
        Returns:
            x (int) -- x coordinate +/- 1
            y (int) -- y coordinate +/- 1
        """
        if random.random() < 0.5:
            self.y = (self.y + 1) % 100
        else:
            self.y = (self.y - 1) % 100
                    
        if random.random() < 0.5:
            self.x = (self.x + 1) % 100
        else:
            self.x = (self.x - 1) % 100
        
    #Make the agents eat the DEM
    def eat(self):
        """
        Transfer data from environment to agent if environment > 10.
        
        Requires no setup.
        
        Returns:
            environment (int) -- environmental data - 10
            store (int) -- data in storage + 10
        """
        if self.environment[self.y][self.x] > 10: #if DEM value >10
            self.environment[self.y][self.x] -= 10 #take 10 away from DEM
            self.store += 10 #and add 10 to agent storage
    
    #returns the distance between 2 agents using pythagoras
    #used in share_with_neighbours
    def distance_between(self, agent):
        """
        Calculates the distance between agents.
        
        Args:
            agent (int) -- information associated with other agents in
                the environment
        
        Returns:
            (float) -- distance between agents
        """
        return (((self.x - agent.x)**2) + ((self.y - agent.y)**2))**0.5

    #Share resources between agents
    def share_with_neighbours(self, neighbourhood):
        """
        Shares data equally between two agents.
        
        Args:
            neighbourhood (int, float) -- minimum distance between 
                agents before they share data.
        
        Returns:
            store (int, float) -- equal share of data in storage
        """
        for agent in self.agents:
            dist = self.distance_between(agent)
            if dist <=  neighbourhood: #if agents are within range
                total = self.store + agent.store #combine storage
                self.store = total / 2 #and split equally between agents
                agent.store = total / 2
import java.io.IOException;
import java.util.StringTokenizer;
import java.util.TreeMap;
import java.util.HashMap;
import java.util.Map;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class TopN {

  public static class TopNMapper
       extends Mapper<LongWritable, Text, Text, IntWritable>{

	private TreeMap<Long, String> tmap;
	  
    private final static IntWritable one = new IntWritable(1);
    private Text word = new Text();
	
	@Override
	public void setup(Context context) throws IOException, InterruptedException {
	    tmap = new TreeMap<Long, String>();
	}

	@Override
    public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
  
	    StringTokenizer itr = new StringTokenizer(value.toString());
	    
	    HashMap<String, Integer> freq = new HashMap<String, Integer>();
	    
	    while (itr.hasMoreTokens()) {
	        word.set(itr.nextToken());
	        freq.putIfAbsent(word.toString(), 0);
	        freq.put(word.toString(), freq.get(word.toString()) + 1);
	      }
	    
	    HashMap.Entry<String, Integer> maxEntry = null;
	    
	    for (HashMap.Entry<String, Integer> entry : freq.entrySet()) {
	    	if (maxEntry == null || entry.getValue().compareTo(maxEntry.getValue()) > 0)
	        {
	            maxEntry = entry;
	        }
	    }
  
        tmap.put( (long) maxEntry.getValue(), maxEntry.getKey());
  
        // we remove the first key-value
        // if it's size increases 5
        if (tmap.size() > 5)
        {
            tmap.remove(tmap.firstKey());
        }
    }
	
	@Override
    public void cleanup(Context context) throws IOException,
                                       InterruptedException
    {
        for (Map.Entry<Long, String> entry : tmap.entrySet()) 
        {
  
            long count = entry.getKey();
            String name = entry.getValue();
  
            context.write(new Text(name), new IntWritable((int)count));
        }
    }
  }

  public static class TopNReducer
       extends Reducer<Text,IntWritable,Text,IntWritable> {

	  private TreeMap<Long, String> tmap2;
	  
	    @Override
	    public void setup(Context context) throws IOException,
	                                     InterruptedException
	    {
	        tmap2 = new TreeMap<Long, String>();
	    }
	  
	    @Override
	    public void reduce(Text key, Iterable<IntWritable> values,
	      Context context) throws IOException, InterruptedException
	    {
	        String word = key.toString();
	        long count = 0;
	  
	        for (IntWritable val : values)
	        {
	            count = val.get();
	        }
	  
	        tmap2.put(count, word);
	  
	        // we remove the first key-value
	        // if it's size increases 5
	        if (tmap2.size() > 5)
	        {
	            tmap2.remove(tmap2.firstKey());
	        }
	    }
	  
	    @Override
	    public void cleanup(Context context) throws IOException,
	                                       InterruptedException
	    {
	  
	        for (Map.Entry<Long, String> entry : tmap2.entrySet()) 
	        {
	  
	            long count = entry.getKey();
	            String name = entry.getValue();
	            context.write(new Text(name), new IntWritable((int)count));
	        }
	    }
  }

  public static void main(String[] args) throws Exception {
    if (args.length != 2) {
    	System.err.println("Usage: TopN <input path> <output path>");
    	System.exit(-1);
    }
    
    Configuration conf = new Configuration();
    Job job = Job.getInstance(conf, "TopN");
    job.setJarByClass(TopN.class);
    
    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));
    
    job.setMapperClass(TopNMapper.class);
    job.setReducerClass(TopNReducer.class);
    
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(IntWritable.class);
    
    System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}